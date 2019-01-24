from . import keys

# Dark Sky URLs
DARK_SKY_API: str = f'https://api.darksky.net/forecast/{keys.DS_TOK}/{{latitude}},{{longitude}},{{time}}'  # noqa: E501
DARK_SKY_HEADER: dict = {'Accept-Encoding': 'gzip'}

# Wit URLs
WIT_URL: str = 'https://api.wit.ai/'
WIT_VER: str = '20170307'

WIT_MESSAGE_API: str = f'{WIT_URL}message'
WIT_HEADER: dict = {'Authorization': f'Bearer {keys.WIT_TOK}',
                    'Accept': f'application/vnd.wit.{WIT_VER}+json'}
