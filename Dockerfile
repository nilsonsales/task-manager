# Use a lightweight Ubuntu base image
FROM ubuntu:22.04 AS base

# Set the working directory inside the container
WORKDIR /app

# Copy the files from the current directory to the container
COPY . /app

# Optionally, you can run any commands necessary to setup your project
# For example, if you need to install dependencies, you can use the RUN instruction
RUN apt update && apt install -y python3 python3-pip && apt clean
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose any ports that your application might be using
# For example, if your application runs on port 8080, you can use the EXPOSE instruction
EXPOSE 8080

# Specify the command to run when the container starts
# For example, if your application is a Python script, you can use the CMD instruction
ENTRYPOINT ["python3", "run.py"]