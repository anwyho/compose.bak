import compose.utils.keys as keys

# Graph & Messenger URLs
GRAPH_API: str = 'https://graph.facebook.com/'
GRAPH_VER: str = 'v2.7'
MESSENGER_PLATFORM: str = f'{GRAPH_API}{GRAPH_VER}/me/'
AUTH: str = f'access_token={keys.FB_PAGE_ACCESS}&appsecret_proof={keys.gen_app_secret_proof()}'  # noqa: E501

MESSAGES_API: str = f'{MESSENGER_PLATFORM}messages?{AUTH}'
MESSAGE_ATTACHMENTS_API: str = f'{MESSENGER_PLATFORM}message_attachments?{AUTH}'  # noqa: E501
MESSENGER_PROFILE_API: str = f'{MESSENGER_PLATFORM}messenger_profile?{AUTH}'
MESSENGER_USER_API: str = f'{GRAPH_API}{{fbId}}?{AUTH}'

# Wit URLs
WIT_URL: str = 'https://api.wit.ai/'
WIT_VER: str = '20170307'

WIT_MESSAGE_API: str = f'{WIT_URL}message'
WIT_HEADER: dict = {'Authorization': f'Bearer {keys.WIT_TOK}',
                    'Accept': f'application/vnd.wit.{WIT_VER}+json'}

# Testing
LOCALHOST = "https://localhost:5000/webhook"
AWS_WEBHOOK = \
    "https://ick416py79.execute-api.us-west-1.amazonaws.com/dev/webhook"
