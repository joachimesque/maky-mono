# Maky Mono

## Install

Create a `venv` and activate it, then install the required dependencies.

```
python3 -m venv ./env
source ./env/bin/activate
pip install -r requirements.txt
```

### Get your secrets!

#### Telegram

Go talk to [Botfather](https://t.me/botfather) and create your own new bot. It’ll give you the bot token.

#### Twitter

- Get a [Twitter Developer profile](https://developer.twitter.com/en/portal/dashboard).
- Create a new project
- Create a new app
- Paste the API key and API secret in the config (under the name `consumer_key` and `consumer_key_secret`)
- In the App permissions, select “Read and Write”
- Create a new set of Access token & secret, and paste them in the config (under the names `access_token` and `access_token_secret`)

## Usage

Activate venv

```
source env/bin/activate
```