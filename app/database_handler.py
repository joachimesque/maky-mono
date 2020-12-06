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

db.generate_mapping(create_tables=True)

@db_session
def add_message(message):
    Message(message=message, created_at=datetime.datetime.now(datetime.timezone.utc))
    return True

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
    message = Message.get(id=message_id)
    message.published_at = datetime.datetime.now(datetime.timezone.utc)
    commit()
