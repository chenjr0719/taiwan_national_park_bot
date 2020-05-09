# Taiwan National Park Bot

A bot to help you send the application for Taiwan National Park permits.

## Installation

This bot requires **Python >= 3.6**.
Please install it by:

```shell
git clone git@github.com:chenjr0719/taiwan_national_park_bot.git
cd taiwan_national_park_bot
pip install .
```

Or, just run it in a Docker container:

```shell
git clone git@github.com:chenjr0719/taiwan_national_park_bot.git
cd taiwan_national_park_bot
./scripts/build.sh
```

## Usage

Before using the bot, please make sure you already create a drfat on https://npm.cpami.gov.tw.
Then, your **ID** and **email** in environment variable:
```shell
export ID=...
export EMAIL=...
```

Or, create a `.env` file and run the Docker container with it:
```shell
./scripts/run.sh
```
