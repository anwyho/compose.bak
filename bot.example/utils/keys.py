import os

# Facebook Page ID
FB_PID: str = os.environ.get('FB_PID', '<PAGE_ID>')

# Debug
DEBUG_TOK: str = os.environ.get('DEBUG_TOK', 'No debug token found.')
