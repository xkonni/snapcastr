# snapcastr

 webinterface to control snapcast server
 written in python with flask, wtforms and python-snapcast, see dependencies.

## features

### main
* see status
![main](https://github.com/xkonni/snapcastr/blob/master/doc/main.png)

### clients
* change volume
![clients](https://github.com/xkonni/snapcastr/blob/master/doc/clients.png)

### groups
* change stream
![groups](https://github.com/xkonni/snapcastr/blob/master/doc/groups.png)

### streams
* see status
![streams](https://github.com/xkonni/snapcastr/blob/master/doc/streams.png)

## getting started

### install
```
git clone https://github.com/xkonni/snapcastr
cd snapcastr
change server address in snapcastr.py
pip install .
```

### run/debug
to just run the application
```
snapcastrd --host=0.0.0.0 --port=5011
```

to debug it
```
export FLASK_APP=snapcastr
export FLASK_DEBUG=true
flask run --host=0.0.0.0 --port=5011
```

### use
open localhost:5011 in browser

## dependencies
* [python](https://www.python.org/)
* [flask](http://flask.pocoo.org/)
* [python-snapcast]( https://github.com/happyleavesaoc/python-snapcast)


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
