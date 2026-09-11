from urllib.parse import urlparse

def detect_source(value: str) -> str:
    host = urlparse(value).netloc.lower()
    if 'youtube.com' in host or 'youtu.be' in host: return 'youtube'
    if 'twitch.tv' in host: return 'twitch'
    return 'unknown'
