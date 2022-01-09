FROM python:3.7-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    gcc \
    python3-dev 


# Create working directory and copy all files
COPY . /app
WORKDIR /app

# Pip install requirements
RUN pip install --user -r requirements.txt

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "main.py"]
