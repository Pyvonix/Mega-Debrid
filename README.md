<h1 align="center"><img style="padding:0;vertical-align:bottom;" height="32" width="32" src="./megadebrid/web/static/favicon.png"/> Mega-Debrid</h1>
<div align="center">
 <p>
   <strong>Your Command-Line Interface and containers to automatically interoperate with <a href="https://www.mega-debrid.eu/">mega-debrid.eu</a></strong>
  </p>
</div>

This [Mega-Debrid](https://github.com/Pyvonix/Mega-Debrid) project provides three asynchronous libs that allow to interact in different ways with [Mega-Debrid.eu](https://www.mega-debrid.eu/) endpoints.

**Disclaimer:** this project **is NOT** an official [Mega-Debrid.eu](https://www.mega-debrid.eu/)'s project or support. It's just my personal implementation that I share with the community.

## Mega-Config

Configurations / credentials on [Mega-Debrid.eu](https://www.mega-debrid.eu/) can be used in two different ways: environment variables or config file.

 - Environment variables examples

```bash
# CREDENTIALS environment variables
export MEGA_USER='user'
export MEGA_PASSWD='password'
# API environment variables
export MEGA_TOKEN='XXXXXXXXXXXXXXXXXXXXXXXXXX'
# AJAX environment variables
export MEGA_USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
export MEGA_COOKIES='{"PHPSESSID":"CCCCCCCCCCCCCCCCCCCCCCCCCC", "11111111111111111111111111111111":"1234567890123456", "22222222222222222222222222222222":"12345678901234567890123456789012345678901234"}'
```

 - Config example: `~/.mega/config`

```ini
[CREDENTIALS]
Username = user
Password = password

[API]
TOKEN = XXXXXXXXXXXXXXXXXXXXXXXXXX

[AJAX]
USER-AGENT = Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko
PHPSESSID = CCCCCCCCCCCCCCCCCCCCCCCCCC
11111111111111111111111111111111 = 1234567890123456
22222222222222222222222222222222 = 12345678901234567890123456789012345678901234
```

## Mega-Libs

 - Explanation / Definition

The following objects inherit from the [MegaDebrid](./megadebrid/libs/base.py) base object and only define asynchronous methods:
 1. [MegaDebridAjax](./megadebrid/libs/ajax.py): interact with `index.php?ajax=<action>` as a REST endpoint to provide asynchronous functions for each action.
    This is the result of the analysis of the AJAX behavior on the [Mega-Debrid.eu](https://www.mega-debrid.eu/) website.
 2. [MegaDebridApi](./megadebrid/libs/api.py): interact with `api.php?action=<action>` as a REST API endpoint to provide asynchronous functions for each action.
    This is a use of the official API follows the [Mega-Debrid API](https://www.mega-debrid.eu/index.php?page=api) documentation.
 3. [MegaDebridFlow](./megadebrid/libs/flow.py): evolved usage of `MegaDebridApi` which isn't longer *"simple"* use of the REST API endpoints, but a complete instrumentalization of different operations: this will chain the requests to obtain the desired result.

 - Code Integration Example

```py
import asyncio

from megadebrid.libs.api import MegaDebridApi


async def async_func():
    async with MegaDebridApi() as megadebrid:
        response = await megadebrid.get_torrents_list()
        return response
```
Note: integration is the same for `MegaDebridApi` and `MegaDebridAjax`, only available methods could change.

## Mega-CLI

 - Explanation

Mega-CLI is the command line tool that allows to use asynchronous libraries without developing any Python line.

 - CLI Standalone

Not all components of the project are required to only use the CLI.
Here are the files needed to use only the CLI:
```
.
├── mega-cli.py
├── README.md
├── requirements-cli.txt
└── megadebrid
    ├── libs
    │   ├── ajax.py
    │   ├── api.py
    │   ├── base.py
    │   └── flow.py
    ├── parsers
    │   ├── argparser.py
    │   └── configparser.py
    └── utils
        ├── decorators.py
        └── progressions.py
```

 - Usage

```bash
usage: mega-cli.py [-h] [-c CONFIG] {ajax,api,flow} ...

Mega-CLI is the command line tool to interact with the different supported backends on Mega-Debrid.eu.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path for the config file (default: ~/.mega/config)

Mega-Debrid supported backends libs:
  {ajax,api,flow}       choice of method to be use
```

### Mega-CLI: AJAX

The `mega-cli.py ajax` will instrumentalize the [MegaDebridAjax](./megadebrid/libs/ajax.py) object by passing the correct given arguments to the called method.

 - Requirements

To use Mega-Debrid AJAX backend, you need to provide yours **Cookies** (particularly: `PHPSESSID`) and the same **User Agent** used during your authentication (the Apache backend requires the same user-agent than has generated the `PHPSESSID`).
This can be done through environment variables: `MEGA_USER_AGENT` & `MEGA_COOKIES`, or your config file `~/.mega/config` section `[AJAX]`.

__Note:__ cookies have a very long lifespan.

 - Usage

```bash
usage: mega-cli.py ajax [-h] {my-torrents,list,torrents,torrent-status,status,upload-magnet,magnet,upload-torrent,torrent,remove-torrent,remove,debrid-link,debrid,link} ...

optional arguments:
  -h, --help            show this help message and exit

Mega-AJAX commands:
  List of commands available on Mega-Debrid AJAX backend

  {my-torrents,list,torrents,torrent-status,status,upload-magnet,magnet,upload-torrent,torrent,remove-torrent,remove,debrid-link,debrid,link}
    my-torrents (list, torrents)
                        get user torrents list
    torrent-status (status)
                        get the status of a torrent
    upload-magnet (magnet)
                        add a magnet link
    upload-torrent (torrent)
                        Add a torrent file
    remove-torrent (remove)
                        remove a torrent from active torrents
    debrid-link (debrid, link)
                        debrid links
```

### Mega-CLI: API

The `mega-cli.py api` will instrumentalize the [MegaDebridApi](./megadebrid/libs/api.py) object by passing the correct given arguments to the called method.

 - Requirement

To use Mega-Debrid API backend, you need to provide your **API Token** which is returned after submitting your username and password on connection endpoint.
This can be done through environment variable: `MEGA_TOKEN`, or your config file: `~/.mega/config` section `[API]`.

__Important note:__ the API token has a **REALLY SHORT** lifespan.
That's the reason why, it is recommended to provide yours **credentials** through environment variables: `MEGA_USER` and `MEGA_PASSWD`, or your config file: `~/.mega/config` in section`CREDENTIALS`; it will allow you to take advantage of **renew obsolete token** feature which will automatically re-authenticate you when your token will be expired.

 - Usage

```bash
usage: mega-cli.py api [-h] {connect-user,connect,user-history,history,hosters-list,hosters,my-torrents,list,torrents,torrent-status,status,upload-magnet,magnet,upload-torrent,torrent,debrid-link,debrid,link} ...

optional arguments:
  -h, --help            show this help message and exit

Mega-API commands:
  List of commands available on Mega-Debrid API backend

  {connect-user,connect,user-history,history,hosters-list,hosters,my-torrents,list,torrents,torrent-status,status,upload-magnet,magnet,upload-torrent,torrent,debrid-link,debrid,link}
    connect-user (connect)
                        connect with creditials
    user-history (history)
                        get user download history
    hosters-list (hosters)
                        list availables hosters (no authenticate)
    my-torrents (list, torrents)
                        get user torrents list
    torrent-status (status)
                        get the status of selected torrent
    upload-magnet (magnet)
                        add a magnet link
    upload-torrent (torrent)
                        add a torrent file
    debrid-link (debrid, link)
                        debrided link
```

### Mega-CLI: Flow

The `mega-cli.py flow` will instrumentalize the [MegaDebridFlow](./megadebrid/libs/flow.py) object by passing the correct given arguments to the called method.

 - Requirement

As `MegaDebridFlow` use `MegaDebridApi`, refer to **Mega-CLI: API** requirements: they are applicable.

 - Usage

```bash
usage: mega-cli.py flow [-h] {wait-until-complete,wait,save-file,save,debrid-and-download,download,unrestrict,download-magnet,ddl-magnet,download-torrent,ddl-torrent} ...

optional arguments:
  -h, --help            show this help message and exit

Mega-Flow commands:
  List of commands available for Mega-Debrid advanced flow

  {wait-until-complete,wait,save-file,save,debrid-and-download,download,unrestrict,download-magnet,ddl-magnet,download-torrent,ddl-torrent}
    wait-until-complete (wait)
                        query the status of a torrent until it is completly processed by Torrent Converter
    save-file (save)    download the file at the given URL and save it in the specified folder
    debrid-and-download (download, unrestrict)
                        unrestrict the link and download it to the specified folder
    download-magnet (ddl-magnet)
                        uses the torrent converter with a magnet link, then download the file in the specified folder
    download-torrent (ddl-torrent)
                        uses the torrent converter with a torrent file, then download the file in the specified folder
```

## Mega-Compose

High level presentation of `docker-compose.yml` to understand each component spawned with Docker.

### Mega-Redis

Redis container used as backend by Celery.

__Note:__ Redis is used by Celery as [result_backend](https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-settings) too, require adding `celery[redis]` in `requirements.txt` or `pip install celery[redis]`.

### Mega-Worker

[Celery](https://docs.celeryq.dev/en/stable/index.html) worker which will handle tasks creation and processing until they are complete.

__Note:__ Celery for this project will use by default `redis` as [result_backend](https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-settings). Otherwise you want persistent results, you could use `sqlite3` as [result_backend](https://docs.celeryq.dev/en/stable/userguide/configuration.html#database-backend-settings). It will require to have `sqlalchemy` in `requirements.txt` or `pip install sqlalchemy`.

 - Launch Celery

```bash
celery -A megadebrid.worker worker -l INFO
```

 - Code Integration Example

```py
from time import sleep

from megadebrid.worker.tasks import save_file, debrid_and_save_file, download_magnet, download_torrent


def launch_task():
    task = debrid_and_save_file.delay('https://1fichier.com/?xxxxxxxxxxxxxxxxxxxx',
                                      '/home/user/Downloads/')

    while tasks.status not in ['SUCCESS', 'FAILURE']:
      print(task.status)
      sleep(1)

    return tasks.result
```

### Mega-Web

[Flask](https://flask.palletsprojects.com/en/2.2.x/cli/) implementation to provide a local API and/or Web interface to allow the user to launch tasks through user-friendly way and track their status.

 - Launched Flask
```bash
flask --app megadebrid.web --debug run -h 0.0.0.0
# or
python manage.py run -h 0.0.0.0
```

 - Web-UI/API usage

#### Task Creation

Request example:
```
POST /tasks HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
Mega-Task: DebridAndSaveFile

{
  "link":"https://1fichier.com/?xxxxxxxxxxxxxxxxxxxx",
  "folder":"/home/user/Downloads",
  "password":""
}
```
`Curl` example:
```bash
curl -H 'Content-Type: application/json' \
     -H 'Mega-Task: DebridAndSaveFile' \
     -d '{"link":"https://1fichier.com/?xxxxxxxxxxxxxxxxxxxx","folder":"/home/user/Downloads","password":""}' \
     -X POST 'http://127.0.0.1:5000/tasks'
```

#### Task Status

Request example:
```
GET /tasks/0de47c5f-3040-475e-9206-9d378f5adbd3 HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json


```
`Curl` example:
```bash
curl -H 'Content-Type: application/json' 'http://127.0.0.1:5000/tasks/0de47c5f-3040-475e-9206-9d378f5adbd3'
```

### Mega-Dashboard (optional)

[Celery flower](https://flower.readthedocs.io/en/latest/) is an optional container, it will be a web based tool for monitoring and administrating Celery clusters. The docker Mega-Dashboard could be pulled for image [mher/flower](https://hub.docker.com/r/mher/flower/) or built with the file `megadebrid/dashboard/Dockerfile`.

__Note:__ require adding `flower` in [requirements.txt](./requirements.txt) to use it throughout [Mega-Docker](./Dockerfile)
