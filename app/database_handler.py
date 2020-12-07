from datetime import (datetime, timezone)
from pathlib import Path

from config import get_config

from pony.orm import (Database,
                      Optional,
                      PrimaryKey,
                      Required,
                      commit,
                      count,
                      db_session,
                      desc,
                      select)

db_config = get_config()['db']

db = Database()

if(db_config['type'] == 'sqlite'):
    db_filename = db_config['sqlite']['filename']
    db_filepath = str(Path(__file__).parents[1].joinpath(db_filename))

    db.bind(provider='sqlite', filename=db_filepath, create_db=True)


class Message(db.Entity):
    id = PrimaryKey(int, auto=True)
    created_at = Required(datetime)
    published_at = Optional(datetime)
    message = Required(str, 1000)
    tg_message_id = Required(int, size=32, index='message_id_index')
    tg_date = Required(datetime, index='message_date_index')

db.generate_mapping(create_tables=True)


@db_session
def add_message(message, message_id, date):
    if(not message or not message_id or not date):
        return False

    message_obj = Message(message=message,
                          created_at=datetime.now(timezone.utc),
                          tg_message_id=message_id,
                          tg_date=date)
    commit()

    return message_obj.id


@db_session
def edit_message(message, message_id, date):
    if(not message or not message_id or not date):
        return False

    message_obj = Message.get(id=message_id)

    if(not message_obj):
        return False

    message_obj.message = message
    commit()

    return message_obj.id


@db_session
def get_message_by_id(message_id):
    message_obj = Message.get(id=message_id)

    return message_obj


@db_session
def get_message_by_tg_id(message_id):
    message_obj = Message.get(tg_message_id=message_id)

    return message_obj


@db_session
def get_last_message():
    messages = select(m for m in Message).order_by(desc(Message.created_at))
    message = messages.first()

    return message


@db_session
def get_next_message():
    all_messages = select(m for m in Message if m.published_at is None)
    all_messages = all_messages.order_by(Message.created_at)

    if(count(all_messages) > 0):
        first_message = all_messages[:1][0]
        return first_message
    else:
        return None


@db_session
def invalidate_message(message_id):
    message = Message.get(id=message_id)
    message.published_at = datetime.now(timezone.utc)
    commit()


@db_session
def delete_message(message_id):
    message = Message.get(id=message_id)
    message.delete()
    commit()
