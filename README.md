# Chat

Educational chat client and server using tkinter and Socket.IO.

## Dev (local) mode

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
python run.py --dev
```
Run the client:

```
python run.py Nickname --dev
```

### Running using a custom URL

Run the server:

```
python run.py --dev --host local.dev --port 8080
```

Run the client:

```
python run.py Nickname --dev --url http://local.dev:8080
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
python run.py --dev --keyfile private.pem --certfile cacert.pem
```

Run the client:

```
python run.py Nickname --dev --url https://localhost:5000
```