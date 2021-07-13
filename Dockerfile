FROM tiangolo/uvicorn-gunicorn:python3.8

# SSH password
ENV SSH_PASSWD "root:Docker!"

WORKDIR /app

COPY . .

# Install needed packages for SSH
RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get update \
    && apt-get install -y --no-install-recommends sudo openssh-server \
    && echo "$SSH_PASSWD" | chpasswd 

# Install Python packages
RUN pip install -r requirements.txt

# Copy over the default SSHD config and entrypoint bash script
COPY sshd_config /etc/ssh/
COPY init_container.sh /opt/

# Set up the user and its group
RUN groupadd -r nonroot && useradd -m -g nonroot nonroot \
    && echo "nonroot ALL=(ALL:ALL) NOPASSWD: /usr/sbin/service ssh start, /usr/sbin/service ssh stop, /usr/sbin/service ssh status, /etc/init.d/ssh start, /etc/init.d/ssh stop, /etc/init.d/ssh status" >> /etc/sudoers \
    && chown -R nonroot:nonroot /app/ \
    && chmod 755 /opt/init_container.sh \
    && chmod a+w /etc/ssh/sshd_config

# Change to nonroot user
USER nonroot

ENV SSH_PORT 2222
EXPOSE 8000 2222

# Run the bash script to start Flask
ENTRYPOINT [ "/opt/init_container.sh" ]