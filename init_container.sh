#!/bin/sh
set -e

cp /etc/ssh/sshd_config /tmp
sed -i "s/SSH_PORT/$SSH_PORT/g" /tmp/sshd_config
cp /tmp/sshd_config /etc/ssh/sshd_config

echo "Starting SSH.."
sudo /usr/sbin/service ssh start

# Start FastAPI with uvicorn
exec uvicorn app:app --host 0.0.0.0 --port 8000
