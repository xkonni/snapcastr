import argparse
import json
import os
from snapcastr.snapcastr import Snapcastr
from xdg import XDG_CONFIG_HOME

CONFIG_FILE = f"{XDG_CONFIG_HOME}/snapcastr.json"
HOST="0.0.0.0"
PORT=5000
SC_HOST="localhost"

def setup():
    parser = argparse.ArgumentParser(description='snapcastr')
    parser.add_argument('--host', metavar='host', type=str, help='webinterface host')
    parser.add_argument('--port', '-p', metavar='port', type=int, help='webinterface port')
    parser.add_argument('--sc_host', '-s', metavar='sc_host', type=str, help='snapcast host')
    parser.add_argument("-c", "--config", dest="config", type=str, help="config file",
        default=CONFIG_FILE)
    parser.add_argument("-d", "--debug", dest="debug", action="store_true",
        help="debug mode")
    args = parser.parse_args()

    # initialize config
    if not os.path.exists(XDG_CONFIG_HOME):
        os.makedirs(XDG_CONFIG_HOME)
    config = {}
    try:
        config_file =  open(args.config, "r")
        config = json.load(config_file)
    except:
        pass

    # fill new keys with defaults
    if not config.get("host"):
        config["host"] = HOST
    if not config.get("port"):
        config["port"] = PORT
    if not config.get("sc_host"):
        config["sc_host"] = SC_HOST

    # overwrite with arguments
    if args.host:
        config["host"] = args.host
    if args.port:
        config["port"] = args.port
    if args.sc_host:
        config["sc_host"] = args.sc_host

    # save to file
    with open(args.config, "w") as config_file:
        json.dump(config, config_file)

    # temporary option
    if args.debug:
        config["debug"] = args.debug
    else:
        config["debug"] = False

    return config

def main():
    config = setup()
    sc = Snapcastr(host=config.get("host"), port=config.get("port"),
            sc_host=config.get("sc_host"), debug=config.get("debug"))
    sc.run()

if __name__ == "__main__":
    main()
