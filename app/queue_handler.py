from database_handler import get_next_message, invalidate_message

message_obj = get_next_message()

if(message_obj):
  print(message_obj.message)
  invalidate_message(message_id=message_obj.id)
else:
  print('No message')