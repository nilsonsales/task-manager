# Use a lightweight Ubuntu base image
FROM ubuntu:22.04 AS base

# Set the working directory inside the container
WORKDIR /app

# Copy the files from the current directory to the container
COPY . /app

# Optionally, you can run any commands necessary to setup your project
RUN apt update && apt install -y python3 python3-pip && apt clean
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose any ports that your application might be using
EXPOSE 8080

# Specify the command to run when the container starts
ENTRYPOINT ["python3", "run.py"]