# snapcastr

## introduction

Snapcastr is a webinterface to control a [snapcast](https://github.com/badaix/snapcast/)
server.

It is written in python with flask, wtforms and python-snapcast

- [python 3](https://www.python.org/)
- [flask](http://flask.pocoo.org/)
- [wtforms](https://wtforms.readthedocs.io)
- [python-snapcast]( https://github.com/happyleavesaoc/python-snapcast)

install from [source](https://github.com/xkonni/snapcastr#install-from-source) or from
[pypi](https://github.com/xkonni/snapcastr#install-from-pypi)


## install from source

### requirements

use your package manager, e.g. apt or pacman and install

- python3
- poetry

### get source

```bash
$ git clone https://github.com/xkonni/snapcastr
```

### install locally

```bash
$ cd snapcastr
$ poetry install
```

### install system-wide

```bash
$ cd snapcastr
$ poetry build
$ sudo pip3 install dist/snapcastr-0.1.0.tar.gz
```


## install from pypi

### install locally

```bash
$ pip install snapcastr
```

### install system-wide

```bash
$ sudo pip install snapcastr
```

## run

### show help

```bash
$ snapcastrd -h

usage: snapcastrd [-h] [--host host] [--port port] [--sc_host sc_host] [-c CONFIG] [-d]

snapcastr

optional arguments:
  -h, --help            show this help message and exit
  --host host           webinterface host
  --port port, -p port  webinterface port
  --sc_host sc_host, -s sc_host
                        snapcast host
  -c CONFIG, --config CONFIG
                        config file
  -d, --debug           debug mode
```

### run the application

- when installed locally

```bash
$ cd snapcastr
$ poetry run snapcastrd --sc_host=address_of_your_snapserver
```

- when installed system-wide

```bash
$ snapcastrd --sc_host=address_of_your_snapserver
```

The `address_of_your_snapserver` might be 127.0.0.1 or localhost, if you are running
snapcastr on the same machine as your snapserver. Snapcastr doesn't need to run with super
user privileges (so you don't need to run it with `sudo`).

### config
The last used configuration is saved in `$HOME/.config/snapcastr.json` and can also be
edited.


## access webinterface

When the application is running, open [http://localhost:5000](http://localhost:5000) in
your browser.


## features

### main screen
* View general status, number of clients, streams, groups of clients
![main](https://github.com/xkonni/snapcastr/blob/master/doc/main.png)

### clients
* View connected clients and change their volume
![clients](https://github.com/xkonni/snapcastr/blob/master/doc/clients.png)

### groups
* View the groups and the stream being played by each group
![groups](https://github.com/xkonni/snapcastr/blob/master/doc/groups.png)

### streams
* View the status of the various streams available
![streams](https://github.com/xkonni/snapcastr/blob/master/doc/streams.png)


## roadmap, in no particular order

### clients
* rename
* remove old

### groups
* rename
* remove
* add

### streams
* rename
