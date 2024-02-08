import json

from pyrogram.types import Message


def get_file_bytes_by_path(path):
    return open(path, 'rb')


def get_dumped_data(data: list[dict[str, str]]):
    try: return json.dumps(data, ensure_ascii=False)
    except: return json.dumps([], ensure_ascii=False)


def get_loaded_data(data: str):
    try: return json.loads(data)
    except: return []


def get_media_duration(message: Message, media_type: str):
    duration = 10

    match media_type:
        case 'audio':
            duration = message.audio.duration
        case 'video':
            duration = message.video.duration
        case 'voice':
            duration = message.voice.duration
        case 'video_note':
            duration = message.video_note.duration

    return duration
