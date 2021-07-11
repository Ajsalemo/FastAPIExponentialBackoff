FROM tiangolo/uvicorn-gunicorn:python3.8

# SSH password
ENV SSH_PASSWD "root:Docker!"

WORKDIR /app

COPY . .

# Install needed packages for SSH
RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "$SSH_PASSWD" | chpasswd \
    && chmod +x /app/init_container.sh

RUN pip install -r requirements.txt
COPY sshd_config /etc/ssh/
EXPOSE 8000 2222

# Run the bash script to start Flask
ENTRYPOINT [ "/app/init_container.sh" ]