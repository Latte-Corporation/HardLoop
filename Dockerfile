### 1. Get Linux
FROM alpine:3.20.2

### 2. Get gcc, musl-dev, libffi-dev, openssl-dev, python3-dev
RUN apk update \
    && apk upgrade \
    && apk add --no-cache bash \
    && apk add --no-cache --virtual=build-dependencies unzip \
    && apk add --no-cache curl \
    && apk add --no-cache gcc \
    && apk add --no-cache musl-dev \
    && apk add --no-cache libffi-dev \
    && apk add --no-cache openssl-dev \
    && apk add --no-cache python3-dev

### 3. Get Java via the package manager
RUN apk update \
    && apk upgrade \
    && apk add --no-cache bash \
    && apk add --no-cache --virtual=build-dependencies unzip \
    && apk add --no-cache curl \
    && apk add --no-cache openjdk21-jre

### 4. Get Python, PIP
RUN apk add --no-cache python3 py3-pip

### 5. Get Poetry and ensure it's in PATH
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

### 6. Set the working directory
WORKDIR /hardloop

### 7. Copy the files
COPY hardloop/pyproject.toml hardloop/poetry.lock ./
COPY hardloop/hardloop ./hardloop
RUN touch README.md

### 8. Create folder for old worlds
RUN mkdir -p /hardloop/old_worlds

### 9. Install the dependencies
RUN poetry install --no-dev

### 10. Copy the server properties
COPY server.properties /hardloop/server.properties

### 11. Expose the port
EXPOSE 25565

### 12. Run the script
CMD ["poetry", "run", "python", "-m", "hardloop.main"]
