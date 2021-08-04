FROM ubuntu:16.04
RUN apt-get update
RUN apt-get -y install python \
             python3 \
             wget \
             bash \
             net-tools \
             netbase \
             strace \
             iproute2 \
             iputils-ping \
             pciutils \
             vim
RUN wget --no-check-certificate https://trex-tgn.cisco.com/trex/release/v2.90.tar.gz && \
    tar -zxvf v2.90.tar.gz -C / && \
    chown root:root /v2.90  && \
    rm v2.90.tar.gz
COPY trex_cfg.yaml /etc/trex_cfg.yaml
WORKDIR /v2.90
CMD ip link add veth1 type veth peer name veth2 && \
    ip link set veth1 up && \
    ip link set veth2 up && \
    ./t-rex-64 -i