from pathlib import Path
import datetime
from pony.orm import *

from config import get_config
db_config = get_config()['db']

db = Database()

if(db_config['type'] == 'sqlite'):
  db_filename = db_config['sqlite']['filename']
  db_filepath = str(Path(__file__).parents[1].joinpath(db_filename))

  db.bind(provider='sqlite', filename=db_filepath, create_db=True)

class Message(db.Entity):
    id = PrimaryKey(int, auto=True)
    created_at = Required(datetime.datetime)
    published_at = Optional(datetime.datetime)
    message = Required(str, 1000)
    tg_message_id = Required(int, size=32, index='message_id_index')
    tg_date = Required(datetime.datetime, index='message_date_index')

db.generate_mapping(create_tables=True)

@db_session
def add_message(message, message_id, date):
  if(not message or not message_id or not date):
    return False

  Message(message=message,
          created_at=datetime.datetime.now(datetime.timezone.utc),
          tg_message_id=message_id,
          tg_date=date
         )
  return True

@db_session
def edit_message(message, message_id, date):
  if(not message or not message_id or not date):
    return False

  message_obj = Message.get(tg_message_id = message_id)

  if(not message_obj):
    return False

  message_obj.message = message
  commit()
  return True

@db_session
def get_message_by_id(message_id):
  if(not message_id):
    return False

  message_obj = Message.get(tg_message_id = message_id)

  return message_obj

@db_session
def get_last_message():
  message = select(m for m in Message).order_by(desc(Message.created_at)).first()

  return message

@db_session
def get_next_message():
  all_messages = select(m for m in Message if m.published_at == None).order_by(Message.created_at)
  
  if(count(all_messages) > 0):
    first_message = all_messages[:1][0]
    return first_message
  else:
    return None

@db_session
def invalidate_message(message_id):
  message = Message.get(id = message_id)
  message.published_at = datetime.datetime.now(datetime.timezone.utc)
  commit()
