from . import keys

# Dark Sky URLs
DARK_SKY_API: str = f'https://api.darksky.net/forecast/{keys.DS_TOK}/{{latitude}},{{longitude}},{{time}}'  # noqa: E501
DARK_SKY_HEADER: dict = {'Accept-Encoding': 'gzip'}
