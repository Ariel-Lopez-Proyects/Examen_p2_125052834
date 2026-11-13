#!/bin/bash
mkdir -p ~/.ssh
cp /keys/id_ed25519 ~/.ssh/id_ed25519
chmod 600 ~/.ssh/id_ed25519
ssh -o StrictHostKeyChecking=no -o PasswordAuthentication=no hadoop@hadoop 'echo "Conectado a $(hostname) como $(whoami)"'
