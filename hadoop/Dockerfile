FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk-headless python3 openssh-server openssh-client \
    curl ca-certificates procps \
 && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/lib/jvm/java-17-openjdk-* /usr/lib/jvm/java

ENV HADOOP_VERSION=3.3.6
RUN curl -fsSL https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    | tar -xz -C /opt \
 && ln -s /opt/hadoop-${HADOOP_VERSION} /opt/hadoop

ENV JAVA_HOME=/usr/lib/jvm/java
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh \
 && printf 'export JAVA_HOME=%s\nexport HADOOP_HOME=%s\nexport PATH=$PATH:%s/bin\n' \
    "$JAVA_HOME" "$HADOOP_HOME" "$HADOOP_HOME" > /etc/profile.d/hadoop.sh

RUN useradd -m -s /bin/bash hadoop \
 && mkdir -p /run/sshd /data/output /keys

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/sbin/sshd", "-D", "-e"]
