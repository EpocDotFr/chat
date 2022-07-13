#!/usr/bin/env bash

set -e # Makes any subsequent failing commands to exit the script immediately

echo "Loading env variables from dotenv files"

if [ -f server/.env ]; then
    export $(cat server/.env | xargs)
fi

echo "Pulling latest code version"

git pull

echo "Restarting site"

status=$(curl --basic --user "${ALWAYSDATA_API_TOKEN} account=${ALWAYSDATA_ACCOUNT_NAME}:" --data '' --request POST --silent --output /dev/null --write-out '%{http_code}' "https://api.alwaysdata.com/v1/site/${ALWAYSDATA_SITE_ID}/restart/")

if [ "$status" = 204 ];
then
    echo "Success"
else
    echo "Error occurred when restarting site."
fi
