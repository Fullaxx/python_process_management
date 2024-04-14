#!/usr/bin/env bash

if [ -z "$1" ]; then
  >&2 echo "$0: <number>"
  exit 1
fi

# echo "\$1: $1"

i="$1"
while [ "${i}" -gt 0 ]; do
#  echo -n "$i "
  sleep 1
  i=$(( i-1 ))
done
#echo "done"
