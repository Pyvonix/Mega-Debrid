#  __  __                         _____            _     _                         _  
# |  \/  |                       |  __ \          | |   | |                       | | 
# | \  / | ___  __ _  __ _ ______| |  | | __ _ ___| |__ | |__   ___   __ _ _ __ __| | 
# | |\/| |/ _ \/ _` |/ _` |______| |  | |/ _` / __| '_ \| '_ \ / _ \ / _` | '__/ _` | 
# | |  | |  __/ (_| | (_| |      | |__| | (_| \__ \ | | | |_) | (_) | (_| | | | (_| | 
# |_|  |_|\___|\__, |\__,_|      |_____/ \__,_|___/_| |_|_.__/ \___/ \__,_|_|  \__,_| 
#               __/ |                                                                 
#              |___/                                                                  
# Dockerfile only for flower: celery dashboard (optional)

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

# install dependencies
RUN pip install --upgrade pip
RUN pip install $PIP_INSTALL_OPTIONS -r requirements.txt
RUN pip install $PIP_INSTALL_OPTIONS flower

# Set Python to use UTF-8 encoding rather than ASCII.
ENV LANG="C.UTF-8"

# Command to launch flower dashboard
#CMD [ "celery", "--app", "megadebrid.worker", "flower", "--port=5555" ]
