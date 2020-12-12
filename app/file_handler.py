import mimetypes
from os.path import splitext
from pathlib import Path
from urllib.parse import urlparse

from database_handler import add_image

max_file_size = 20 * (1024 ** 2)


def store_file(bot,
               file_id,
               chat_id,
               update_id,
               message_id,
               mime_type=None):
    if not message_id:
        return('no message with the image :(')

    file = bot.get_file(file_id)

    if file.file_size > max_file_size:
        return(False, 'The image you sent is too big, '
               'try uploading it as an image, not as a document.')

    if mime_type:
        extension = mimetypes.guess_extension(mime_type)
    else:
        mime_type = mimetypes.guess_type(file.file_path)[0]
        path = urlparse(file.file_path).path
        extension = splitext(path)[1]

    download_path = Path(__file__).parents[1].joinpath('uploads', str(chat_id))
    download_path.mkdir(parents=True, exist_ok=True)
    download_path = download_path.joinpath('{}{}'.format(update_id, extension))

    file.download(str(download_path))

    file_path = '{}/{}{}'.format(str(chat_id), update_id, extension)

    image_result = add_image(message_id=message_id,
                             file_path=file_path,
                             mime_type=mime_type)

    if image_result:
        return(True, 'The image was sent.')
    else:
        return(False, 'The image wasn’t uploaded.')


def delete_file(file_path):
    path_to_unlink = Path(__file__).parents[1].joinpath('uploads', file_path)

    path_to_unlink.unlink()
