#!/bin/bash

docker run -it \
  -v $PWD:/melodic \
  -h "in_docker" \
  -p 5901:5901 \
  -p 6901:6901 \
  -v /etc/localtime:/etc/localtime:ro \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=unix$DISPLAY \
  -e GDK_SCALE \
  -e GDK_DPI_SCALE \
  --name melodic \
  --user ubuntu \
  lishuanghua/ros:melodic \
  /bin/bash