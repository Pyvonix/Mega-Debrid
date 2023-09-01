# ___  ___                       ______           _              
# |  \/  |                       |  _  \         | |             
# | .  . | ___  __ _  __ _ ______| | | |___   ___| | _____ _ __  
# | |\/| |/ _ \/ _` |/ _` |______| | | / _ \ / __| |/ / _ \ '__| 
# | |  | |  __/ (_| | (_| |      | |/ / (_) | (__|   <  __/ |    
# \_|  |_/\___|\__, |\__,_|      |___/ \___/ \___|_|\_\___|_|    
#               __/ |                                            
#              |___/                                             
# Dockerfile all in one: flask (web interface) + celery tasks (worker) + flower (celery dashboard)

ARG PIP_INSTALL_OPTIONS="--disable-pip-version-check --no-cache-dir --no-compile --upgrade"

# Pull official Python
FROM python:3.11-alpine
LABEL maintainer="Pyvonix <pyvonix@protonmail.com>"

# Set Mega-Debrid directory
WORKDIR /usr/src

# Copy project source code
COPY . .

# Set Python to force stdin, stdout and stderr to be totally unbuffered.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Mega-Debrid dependencies
RUN pip install --upgrade pip
RUN pip install $PIP_INSTALL_OPTIONS -r requirements.txt

# Set Python to use UTF-8 encoding rather than ASCII.
ENV LANG="C.UTF-8"

# Command to launch Mega-Worker and Mega-Web inside single container
CMD ["/bin/sh", "-c", "echo FIRST COMMAND ; echo SECOND COMMAND"]
