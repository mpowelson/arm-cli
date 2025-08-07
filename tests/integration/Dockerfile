FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    sudo python3 python3-pip docker.io \
    x11-apps xauth && \
    rm -rf /var/lib/apt/lists/*

# Create test user with passwordless sudo
RUN useradd -m testuser && echo "testuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Create docker group
RUN groupadd docker || true && usermod -aG docker testuser

USER testuser
WORKDIR /home/testuser

# Copy project code
COPY . /home/testuser/arm-cli
WORKDIR /home/testuser/arm-cli

# Install arm-cli
RUN pip3 install -e .

ENTRYPOINT ["./integration/run.sh"]
