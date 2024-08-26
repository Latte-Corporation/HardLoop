# syntax=docker/dockerfile:1

################################################################################

# Create a new stage for running the application that contains the minimal
# runtime dependencies for the application. This often uses a different base
# image from the install or build stage where the necessary files are copied
# from the install stage.
#
# The example below uses eclipse-turmin's JRE image as the foundation for running the app.
# By specifying the "22-jre-jammy" tag, it will also use whatever happens to be the
# most recent version of that tag when you build your Dockerfile.
# If reproducability is important, consider using a specific digest SHA, like
# eclipse-temurin@sha256:99cede493dfd88720b610eb8077c8688d3cca50003d76d1d539b0efc8cca72b4.
FROM eclipse-temurin:22-jre-jammy AS final

WORKDIR /build

COPY --chmod=755 server.jar /build/server.jar
COPY --chmod=644 eula.txt /build/eula.txt

EXPOSE 25565

ENTRYPOINT [ "java", "-Xmx1024M", "-Xms1024M", "-jar", "server.jar", "nogui"]
