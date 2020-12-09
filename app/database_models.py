from datetime import datetime

from pathlib import Path

from config import get_config

from pony.orm import (Database,
                      Optional,
                      PrimaryKey,
                      Required,
                      Set)


db_config = get_config()['db']

db = Database()

if(db_config['type'] == 'sqlite'):
    db_filename = db_config['sqlite']['filename']
    db_filepath = str(Path(__file__).parents[1].joinpath(db_filename))

    db.bind(provider='sqlite', filename=db_filepath, create_db=True)


class Message(db.Entity):
    id = PrimaryKey(int, auto=True)
    created_at = Required(datetime, default=lambda: datetime.utcnow())
    published_at = Optional(datetime)
    message = Required(str, 1000)
    tg_message_id = Required(int, size=32, index='message_id_index')
    tg_date = Required(datetime, index='message_date_index')
    images = Set('Image')


class Image(db.Entity):
    id = PrimaryKey(int, auto=True)
    message = Required(Message)
    file_path = Required(str)
    mime_type = Required(str)


db.generate_mapping(create_tables=True)
