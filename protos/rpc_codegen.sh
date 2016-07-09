#!/usr/bin/env bash

protoc --python_out=../script/net/rpc/ --plugin=protoc-gen-grpc=`which grpc_python_plugin` ./rpc.proto -I .