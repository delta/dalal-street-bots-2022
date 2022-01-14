#!/bin/zsh

# cd into the server dir
SCRIPT=$(readlink -f "$0")
cd "$(dirname "$SCRIPT")/../"

# remove the previous proto_build dir
mkdir -p ./app/proto_build
rm -rf ./app/proto_build/*

python3 -m grpc_tools.protoc -I proto --python_out=app/proto_build/ --grpc_python_out=app/proto_build/ ./proto/*.proto
python3 -m grpc_tools.protoc -I proto --python_out=app/proto_build/ ./proto/actions/*.proto
python3 -m grpc_tools.protoc -I proto --python_out=app/proto_build/ ./proto/datastreams/*.proto
python3 -m grpc_tools.protoc -I proto --python_out=app/proto_build/ ./proto/models/*.proto

egrep -rl "^from (actions|datastreams|models)" app/proto_build/ | grep ".py" \
    | xargs sed -r -i.bak 's/^from (actions|datastreams|models) import/from proto_build.\1 import/g'

find . -type f -name "*.bak" -exec rm {} \;