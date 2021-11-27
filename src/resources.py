import json
import threading

config = {}
counts = {}

locks = {
    "config": threading.Lock(),
    "counts": threading.Lock()
}

def reload(filename=None) -> None:
    '''Reloads the specified file. Reloads all files if None is given'''
    global counts, config

    if filename == "config" or filename is None:
        with locks["config"]:
            with open("data/config.json", "r") as config_file:
                config = json.load(config_file)
    
    if filename == "counts" or filename is None:
        with locks["counts"]:
            with open("data/counts.json", "r") as data_file:
                counts = json.load(data_file)

def write(filename: str) -> None:
    '''A function to write out the modified data'''

    if filename == "config":
        with locks["config"]:
            with open("data/config.json", "w") as outfile:
                json.dump(config, outfile)

    elif filename == "counts":
        with locks["counts"]:
            with open("data/counts.json", "w") as outfile:
                json.dump(counts, outfile)
        
    else:
        raise ValueError("Expected a configuration file")


reload(None)
