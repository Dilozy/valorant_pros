import re


def URL_to_ID(video_url):
    # Проверим наличие видео ID в URL с помощью регулярного выражения
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", video_url)
    if match:
        return match.group(1)
    return None

