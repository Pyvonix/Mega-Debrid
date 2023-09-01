#   __  __                      __          __  _      
#  |  \/  |                     \ \        / / | |     
#  | \  / | ___  __ _  __ _ _____\ \  /\  / /__| |__   
#  | |\/| |/ _ \/ _` |/ _` |______\ \/  \/ / _ \ '_ \  
#  | |  | |  __/ (_| | (_| |       \  /\  /  __/ |_) | 
#  |_|  |_|\___|\__, |\__,_|        \/  \/ \___|_.__/  
#                __/ |                                 
#               |___/                                  
# Dockerfile only for flask web interface

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

# Command to launch flask web interface
CMD [ "python", "manage.py", "run", "-h", "0.0.0.0" ]
