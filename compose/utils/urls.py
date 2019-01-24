import compose.utils.keys as keys

# Graph & Messenger URLs
GRAPH_API: str = 'https://graph.facebook.com/'
GRAPH_VER: str = 'v2.6'
MESSENGER_PLATFORM: str = f'{GRAPH_API}{GRAPH_VER}/me/'

# Authentication
ACCESS_TOKEN: str = f'access_token={keys.FB_PAGE_ACCESS}'
APP_SECRET_PROOF: str = f'appsecret_proof={keys.gen_app_secret_proof()}'
AUTH: str = f'{ACCESS_TOKEN}'
AUTH_WITH_PROOF: str = f'{ACCESS_TOKEN}&{APP_SECRET_PROOF}'

# Send API
MESSAGES_API: str = f'{MESSENGER_PLATFORM}messages?{AUTH}'

# Other Messenger APIs
MESSAGE_ATTACHMENTS_API: str = f'{MESSENGER_PLATFORM}message_attachments?{AUTH}'  # noqa: E501
MESSENGER_PROFILE_API: str = f'{MESSENGER_PLATFORM}messenger_profile?{AUTH}'
MESSENGER_USER_API: str = f'{GRAPH_API}{{fbId}}?{AUTH}'
