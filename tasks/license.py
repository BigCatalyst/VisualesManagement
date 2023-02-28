import hashlib
import json
from datetime import datetime
from uuid import getnode as get_mac

import pytz
import requests
from django.conf import settings
from django.utils.timezone import now

from tasks.license_offline import OfflineCache, verify_response_signature
from tasks.models import License

utc = pytz.UTC


def keygen_activation_token(license_id):
    res = requests.post(
        "https://api.keygen.sh/v1/accounts/{ACCOUNT}/licenses/{LICENSE}/tokens".format(
            ACCOUNT=settings.KEYGEN_ACCOUNT_ID, LICENSE=license_id),
        headers={
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
            "Authorization": "Bearer {TOKEN}".format(
                TOKEN=settings.CINEMA_TOKEN)
        },
        data=json.dumps({
            "data": {
                "type": "tokens",
                "attributes": {
                    "maxActivations": 1
                }
            }
        })
    ).json()
    return res["data"]


def validate_license_key(license_key, machine_fingerprint):
    res = requests.post(
        "https://api.keygen.sh/v1/accounts/{}/licenses/actions/validate-key".format(
            settings.KEYGEN_ACCOUNT_ID),
        headers={
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json"
        },
        data=json.dumps({
            "meta": {
                "scope": {"fingerprint": machine_fingerprint},
                "key": license_key
            }
        })
    )

    return res


def activate_license(license_id, license_key):
    last_license, created = License.objects.get_or_create(
        license_id=license_id, key=license_key)
    validation = {}
    machine_fingerprint = hashlib.sha256(
        str(get_mac()).encode('utf-8')).hexdigest()
    try:
        res = validate_license_key(license_key, machine_fingerprint)
        validation = res.json()
        try:
            OfflineCache.write(res)
        except:
            pass
        last_license.created = utc.localize(datetime.fromisoformat(
            validation["data"]["attributes"]["created"].replace("Z", '')))
        last_license.validated = utc.localize(datetime.fromisoformat(
            validation["data"]["attributes"]["lastValidated"].replace("Z", '')))
        if validation["data"]["attributes"]["expiry"]:
            last_license.expired = utc.localize(datetime.fromisoformat(
                validation["data"]["attributes"]["expiry"].replace("Z", '')))
        last_license.save()
    except requests.exceptions.ConnectionError:
        cache_data = OfflineCache.read()
        if cache_data is not None:
            sig, digest, date, body = cache_data
            license_date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT')
            # Verify the cached data
            ok = verify_response_signature(sig, digest, date, body)
            if ok:
                # Respond with the cached data
                validation = json.loads(body)
                if utc.localize(last_license.validated) > now() or utc.localize(last_license.created) > now():
                    return False, "your date is incorrect"
                if utc.localize(last_license.expired) < now() or (now() - utc.localize(license_date)).days > 30:
                    return False, "license expired"
                last_license.validated = now
                last_license.save()
        else:
            return False, "you are offline, please try later"
    if "errors" in validation:
        errs = validation["errors"]

        return False, "license validation failed: {}".format(
            map(lambda e: "{} - {}".format(e["title"], e["detail"]).lower(),
                errs)
        )

    # If the license is valid for the current machine, that means it has
    # already been activated. We can return early.
    if validation["meta"]["valid"]:
        return True, "license has already been activated on this machine"

    # Otherwise, we need to determine why the current license is not valid,
    # because in our case it may be invalid because another machine has
    # already been activated, or it may be invalid because it doesn't
    # have any activated machines associated with it yet and in that case
    # we'll need to activate one.
    #
    # NOTE: the "NO_MACHINE" status is unique to *node-locked* licenses. If
    #       you need to implement a floating license, you may also need to
    #       check for the "NO_MACHINES" status (note: plural) and also the
    #       "FINGERPRINT_SCOPE_MISMATCH" status.
    if validation["meta"]["constant"] != "NO_MACHINE":
        return False, "license {}".format(validation["meta"]["detail"])

    # If we've gotten this far, then our license has not been activated yet,
    # so we should go ahead and activate the current machine.
    token = keygen_activation_token(license_id)["attributes"]["token"]
    activation = requests.post(
        "https://api.keygen.sh/v1/accounts/{}/machines".format(
            settings.KEYGEN_ACCOUNT_ID),
        headers={
            "Authorization": "Bearer {}".format(token),
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json"
        },
        data=json.dumps({
            "data": {
                "type": "machines",
                "attributes": {
                    "fingerprint": machine_fingerprint
                },
                "relationships": {
                    "license": {
                        "data": {"type": "licenses",
                                 "id": validation["data"]["id"]}
                    }
                }
            }
        })
    ).json()

    # If we get back an error, our activation failed.
    if "errors" in activation:
        errs = activation["errors"]

        return False, "license activation failed: {}".format(
            map(lambda e: "{} - {}".format(e["title"], e["detail"]).lower(),
                errs)
        )

    return True, "license activated"
