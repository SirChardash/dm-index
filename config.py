import json
from os.path import exists

config_location = 'config.json'
config = dict()

config_default = {
    'dir': 'C:\\Users\\Chardash\\OneDrive\\Desktop\\Bestiary',
    'theme': 'Light'
}


def initialize():
    if not exists(config_location):
        save()
    global config
    file = open('config.json', 'r')
    config_from_file = json.loads(file.read())
    if config_from_file:
        config = config_from_file
    print(config)


def put(key, value):
    config[key] = value
    save()
    print(config)


def get(key):
    if key in config:
        return config[key]
    elif key in config_default:
        put(key, config_default[key])
    return config[key]


def save():
    file = open('config.json', 'w')
    file.write(json.dumps(config, indent=2))
    file.close()
