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

#### Mastodon

Open the Python console.

```
from mastodon import Mastodon

Mastodon.create_app(
     'YOUR_APP_NAME',
     api_base_url = 'YOUR_INSTANCE_URL'
)
```

This will output a tuple with your `client_id` and `client_secret` (to be added to the config file).

Then,

```
mastodon = Mastodon(
    client_id = YOUR_CLIENT_ID,
    client_secret = YOUR_CLIENT_SECRET,
    api_base_url = 'YOUR_INSTANCE_URL'
)
mastodon.log_in(
    'MY_EMAIL@mail.com',
    'MY_PASSWORD_123'
)
```

The last command returns a string, it is the `access_token` (to be added to the config file).

## Usage

### Cron

Type 

```
crontab -e
```

add this line at the end of the file:

```
30 14 * * * cd /data/profils/joachim/maky-mono && . ./env/bin/activate && python app/queue_handler.py
```

It will post a link from your queue every day at 14:30 (2:30 pm).


### Telegram bot

See https://github.com/python-telegram-bot/python-telegram-bot/wiki/Hosting-your-bot

```
screen -S makymono
```

Then start up the bot

```
source env/bin/activate
python app/telegram_handler.py
```

If you quit the screen (`Ctrl A D`), you can reattach it with `screen -r makymono`.