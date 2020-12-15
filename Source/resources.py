import json

config = {}
role_givers = {}
channel_info = {}


def reload(filename=None) -> None:
    '''Reloads the specified file. Reloads all files if None is given'''
    global config, role_givers, channel_info

    if filename == "config" or filename is None:
        with open("Resources/config.json") as config_file:
            config = json.load(config_file)


def write(filename: str) -> None:
    '''A function to write out the modified data'''

    if filename == "config":
        with open("Resources/config.json", "w") as outfile:
            json.dump(config, outfile)

    else:
        raise ValueError("Expected a configuration file")


reload()
