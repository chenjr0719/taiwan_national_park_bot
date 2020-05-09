#!/bin/bash

BASE_DIR=$(dirname "$0")
PROJECT_DIR=$(cd "$BASE_DIR/.."; pwd -P)

docker run -it --rm \
    --env-file $PROJECT_DIR/.env \
    -v $PROJECT_DIR:/workspace \
    -w /workspace \
    chenjr0719/tnpb
