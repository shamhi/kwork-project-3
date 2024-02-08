from dotenv import dotenv_values


env = dotenv_values()

def getenv(key, ntype, default=None):
    value = env.get(key)
    if not value:
        return default
    return ntype(value)


class Config:
    API_ID = getenv('API_ID', int)
    API_HASH = getenv('API_HASH', str)
    APP_NAME = getenv('APP_NAME', str)
    EDEN_TOKEN = getenv('EDEN_TOKEN', str)
    GLOBAL_ACTION = getenv('GLOBAL_ACTION', str)
