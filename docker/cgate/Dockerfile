# Pull base image
FROM balenalib/raspberrypi3-openjdk:8-jdk

# Copy cgate app into the container
COPY /app /cgate

# Leave logging enabled without filling up the disk
WORKDIR /cgate/logs
RUN ln -s /dev/null event.txt

# Start cgate
WORKDIR /cgate
ENTRYPOINT ["java", "-jar", "cgate.jar"]
