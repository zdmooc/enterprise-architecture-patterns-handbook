# Multi-stage, OCI image and arbitrary-UID compatible.
# Educational image: replace and pin both base images by digest before production.
FROM eclipse-temurin:21-jdk AS compile
WORKDIR /src
COPY src/ /src/
RUN mkdir -p /out && javac --add-modules jdk.httpserver -d /out /src/ExampleServer.java

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=compile /out/ /app/
# /app is read-only at runtime; group 0 permissions support arbitrary OpenShift UID.
RUN chgrp -R 0 /app && chmod -R g=u /app
USER 10001
EXPOSE 8080
ENV PORT=8080 APP_MODE=demo
ENTRYPOINT ["java", "--add-modules", "jdk.httpserver", "-XX:MaxRAMPercentage=70.0", "-cp", "/app", "ExampleServer"]
