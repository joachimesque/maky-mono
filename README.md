# Maky Mono

![Photo of a lemur catta](https://imgur.com/ZhFK6mV)

Maky Mono is a single-user tool to queue messages to be published on Twitter or Mastodon at a later date, the queue is filled by a Telegram bot.

It uses Python 3.

## Set it up!

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

## Start it up!

### Cron

Type 

```
crontab -e
```

add this line at the end of the file:

```
30 14 * * * cd PATH_TO/maky-mono && . ./env/bin/activate && python app/queue_handler.py
```

It will post a link from your queue 
[every day at 14:30 (2:30 pm)](https://crontab.guru/#30_14_*_*_*).


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

## Use it ~~up~~!

Now you can start talking to your Telegram bot (it’s in your contacts since you set it up).

Regular messages get added to the queue.

When you share a link from your mobile OS _Share_ menu along with a comment, Telegram sends two message (one with the comment, followed by the link). Maky will try to detect the double-posting and will add up the two messages so they are published as one. The rule is: if two messages are received less than 3 seconds apart and have consecutive message ID numbers, they are to be published together.

Maky doesn't accept images and media messages _(yet)_.

**Commands:**

- `/show xxx` shows you a message, replace `xxx` with `next` to see the next message that'll be published, `last` to see the last message added to the queue, or the id of any message (it’s a number)
- `/delete xxx` deletes a message. Same values are accepted to replace `xxx` than for `/show`. Displays a warning before deleting a message.
- `/start` has no real function right now.

## About the name

![Photo of a lemur catta](https://imgur.com/ZhFK6mV)

“_Maky_” is the malagasy name for the Lemur Catta, a lemur that lives in Madagascar. 
The tool got this name because the maky has one of the longest tail-to-body ratio among mammals, and « queue » in French means “tail”.
You should know that the maky is endangered. Why not help the conservation efforts, learn more on the [Lemur Conservation Network](https://www.lemurconservationnetwork.org/how-to-help/shop/)!

The photo of the maky was taken by [Mathias Appel](https://www.flickr.com/photos/mathiasappel/25911695040) and is in the public domain. His lemur pictures are amazing, [go see them on Flickr](https://www.flickr.com/photos/144285761@N05/galleries/72157679442235730/).
