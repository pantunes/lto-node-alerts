# LTO Node Alerts

This service sends notifications about Nodes that their balance reached a minimum 
threshold.

These notifications are sent in the Telegram channel [LTO Node Alerts](https://t.me/joinchat/AAAAAFISF9ZjCObeRTmSiw).

## Pre-requisites

* [Python >= 3.7](https://www.python.org/downloads)


## Installation

### Install from source

Clone project repository:
```bash
$ git clone git@github.com:pantunes/lto-node-alerts.git
$ cd lto-node-alerts
```

Setup Python virtual environment:
```bash
$ virtualenv venv -p python3
$ source venv/bin/activate
```

Install package in develop mode:
```bash
pip install -e .
```
(Dependencies will be installed automatically from [requirements.txt](requirements.txt))

## Start services

### Bot

```bash
$ BOT_TOKEN_ID=<bot_id_token> bot
```

### Scheduler

```bash
$ BOT_TOKEN_ID=<bot_id_token> GROUP_CHAT_ID=<GROUP_CHAT_ID> scheduler
```
