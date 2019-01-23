LOCALHOST: str = 'http://localhost:5000/webhook?'
AWSHOST: str = ''

TESTING_LOCALLY: bool = True

TEST_CLIENT: str = ''
TEST_URL: str = ''

if TESTING_LOCALLY:
    TEST_CLIENT = 'localhost'
    TEST_URL = LOCALHOST
else:
    TEST_CLIENT = 'aws'
    TEST_URL = AWSHOST
