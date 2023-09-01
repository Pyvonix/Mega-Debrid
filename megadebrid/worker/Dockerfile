#  __  __                      __          __        _              
# |  \/  |                     \ \        / /       | |             
# | \  / | ___  __ _  __ _ _____\ \  /\  / /__  _ __| | _____ _ __  
# | |\/| |/ _ \/ _` |/ _` |______\ \/  \/ / _ \| '__| |/ / _ \ '__| 
# | |  | |  __/ (_| | (_| |       \  /\  / (_) | |  |   <  __/ |    
# |_|  |_|\___|\__, |\__,_|        \/  \/ \___/|_|  |_|\_\___|_|    
#               __/ |                                               
#              |___/                                                
# Dockerfile only for celery tasks handle and processing

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

# Command to launch celery worker
CMD [ "celery", "-A", "megadebrid.worker", "worker", "-l", "INFO", "--logfile=/var/log/celery.log" ]
