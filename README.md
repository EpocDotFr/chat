# Chat

Educational chat client and server using tkinter and Socket.IO.

## Dev (local) mode

The server is using gevent and gevent-websocket for Socket.IO's websocket transport.

### Install

Server:

```
pip install requirements-dev.txt
```

Client:

```
pip install requirements.txt
```

### Running using defaults

Run the server:

```
export DEV=true
python run.py
```
Run the client:

```
export DEV=true
export NICKNAME=Nickname
python run.py
```

### Running using a custom URL

Run the server:

```
export DEV=true
export HOST=local.dev
export PORT=8080
python run.py
```

Run the client:

```
export DEV=true
export NICKNAME=Nickname
export URL=http://local.dev:8080
python run.py
```

### Running using SSL and defaults

Generate a private key:

```
openssl genrsa -out private.pem 2048
```

Generate a certificate:

```
openssl req -new -x509 -key private.pem -out cacert.pem
```

Run the server:

```
export DEV=true
export KEYFILE=private.pem
export CERTFILE=cacert.pem
python run.py
```

Run the client:

```
export DEV=true
export NICKNAME=Nickname
export URL=https://localhost:5000
python run.py
```

## Production mode

The server is using gevent and the built-in uwsgi's websocket capabilities for Socket.IO's websocket transport.

### Install

Server:

```
pip install requirements-prod.txt
```

Client:

```
pip install requirements.txt
```

### Without SSL

TODO

### With SSL

TODO