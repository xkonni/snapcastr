# snapcastr

 Snapcastr is a webinterface to control a [snapcast](https://github.com/badaix/snapcast/) server.
 
 It is written in python with flask, wtforms and python-snapcast (see [dependencies](https://github.com/xkonni/snapcastr#dependencies)).


## getting started


### install

```

git clone https://github.com/xkonni/snapcastr

cd snapcastr

pip install .

```
You may need to use `pip3 install .` to install properly to a Python 3 path.


### run/debug
#### run
to just run the application

```

snapcastrd --bind=0.0.0.0 --port=5011 --host=address_of_your_snapserver

```
The `address_of_your_snapserver` might be 127.0.0.1 or localhost, if you are running snapcastr on the same machine as your snapserver. Snapcastr doesn't need to run with super user privileges (so you don't need to run it with `sudo`).

#### debug
to debug it

```

export FLASK_APP=snapcastr

export FLASK_DEBUG=true

flask run --host=0.0.0.0 --port=5011

```



### use

Open http://localhost:5011 in your browser.



## dependencies

* [python 3](https://www.python.org/)

* [flask](http://flask.pocoo.org/)

* [python-snapcast]( https://github.com/happyleavesaoc/python-snapcast)



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
