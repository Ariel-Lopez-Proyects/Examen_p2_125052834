#!/bin/bash
set -e

if [ ! -f /keys/id_ed25519 ]; then
  ssh-keygen -q -t ed25519 -N "" -f /keys/id_ed25519
fi

install -d -m 700 -o hadoop -g hadoop /home/hadoop/.ssh
install -m 600 -o hadoop -g hadoop /keys/id_ed25519 /home/hadoop/.ssh/id_ed25519
install -m 644 -o hadoop -g hadoop /keys/id_ed25519.pub /home/hadoop/.ssh/id_ed25519.pub
install -m 600 -o hadoop -g hadoop /keys/id_ed25519.pub /home/hadoop/.ssh/authorized_keys
printf 'Host *\n  StrictHostKeyChecking no\n  UserKnownHostsFile /dev/null\n' > /home/hadoop/.ssh/config
chown hadoop:hadoop /home/hadoop/.ssh/config
chmod 600 /home/hadoop/.ssh/config

sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config

exec "$@"
