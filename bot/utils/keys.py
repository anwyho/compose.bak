import os

# BART
BART_PUBL: str = os.environ.get('BART_PUBL', 'MW9S-E7SL-26DU-VV8V')
BART_PRIV: str = os.environ.get('BART_PRIV', 'No BART private key found.')

# Dark Sky
DS_TOK: str = os.environ.get('DARK_SKY_PRIV', 'No Dark Sky token found.')

# Facebook
FB_PID: str = os.environ.get('FB_PID', '<PAGE_ID>')

# Wit
WIT_TOK: str = os.environ.get('WIT_SERVER_TOK', 'No Wit token found.')

# Debug
DEBUG_TOK: str = os.environ.get('DEBUG_TOK', 'No debug token found.')
