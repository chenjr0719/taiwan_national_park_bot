#!/bin/bash

BASE_DIR=$(dirname "$0")
PROJECT_DIR=$(cd "$BASE_DIR/.."; pwd -P)

if [[ -f $PROJECT_DIR/.env ]]; then
    docker run -it --rm \
        --env-file $PROJECT_DIR/.env \
        -v $PROJECT_DIR:/workspace \
        -w /workspace \
        chenjr0719/tnp_bot
else
    docker run -it --rm \
        -e ID=$ID \
        -e EMAIL=$EMAIL \
        -v $PROJECT_DIR:/workspace \
        -w /workspace \
        chenjr0719/tnp_bot
fi


