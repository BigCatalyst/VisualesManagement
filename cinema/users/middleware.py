from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AdminMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        from tasks.license import activate_license
        from tasks.models import License
        if "admin" in request.get_full_path() and not request.user.is_superuser:
            try:
                _license = License.objects.latest("id")
            except License.DoesNotExist:
                _license = None
            if not _license:
                return redirect("tasks:license")
            else:
                activated, msg = activate_license(_license.license_id,
                                                  _license.key)
                if not activated:
                    return redirect("tasks:license")

        return response
