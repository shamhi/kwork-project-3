from dotenv import dotenv_values


env = dotenv_values()

def getenv(key, ntype, default=None):
    value = env.get(key)
    if not value:
        return default
    return ntype(value)


class Config:
    API_ID1 = getenv('API_ID1', int)
    API_HASH1 = getenv('API_HASH1', str)
    APP_NAME1 = getenv('APP_NAME1', str)

    API_ID2 = getenv('API_ID2', int)
    API_HASH2 = getenv('API_HASH2', str)
    APP_NAME2 = getenv('APP_NAME2', str)

    EDEN_TOKEN = getenv('EDEN_TOKEN', str)
    GLOBAL_ACTION = getenv('GLOBAL_ACTION', str)
