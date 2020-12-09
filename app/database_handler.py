from datetime import (datetime, timezone)

from database_models import (Image, Message)

from pony.orm import (commit,
                      count,
                      db_session,
                      desc,
                      select)


# MESSAGES

@db_session
def add_message(message, message_id, date):
    if(not message or not message_id or not date):
        return False

    message_obj = Message(message=message,
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


# IMAGES

@db_session
def add_image(message_id, file_path, mime_type):
    if(not message_id or not file_path or not mime_type):
        return False

    message_obj = Message.get(id=message_id)

    image_obj = Image(message=message_obj,
                      file_path=file_path,
                      mime_type=mime_type)
    commit()

    return image_obj.id
