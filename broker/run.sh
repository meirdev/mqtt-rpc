#!/usr/bin/env bash

docker run --rm -it -p 1883:1883 -p 9001:9001 -v $PWD/mosquitto.conf:/mosquitto/config/mosquitto.conf -v /mosquitto/data -v /mosquitto/log eclipse-mosquitto:1.6.15
