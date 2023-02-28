@echo off

echo Syncing docker container time…
bash -c “docker run --net=host --ipc=host --uts=host --pid=host --security-opt=seccomp=unconfined --privileged --rm alpine date -s “$(date -u ‘+%%Y-%%m-%%d %%H:%%M:%%S’)””
docker run --privileged -v /var/empty -v /etc/ntpd.conf:/etc/ntpd.conf cinema_celery -f /etc/ntpd.conf -s