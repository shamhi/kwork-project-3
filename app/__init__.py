from os import mkdir
from os.path import isdir


if not isdir('app/downloads/'):
    mkdir('app/downloads')
    with open('app/downloads/media.mp3', 'w') as file:
        ...
