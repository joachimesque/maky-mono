def get_file_info(message):
    if message.document:
        file_id = message.document.file_id
        mime_type = message.document.mime_type
    else:
        file_id = message.photo[-1].file_id
        mime_type = None

    return ({'file_id': file_id, 'mime_type': mime_type})
