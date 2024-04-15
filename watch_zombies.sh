#!/bin/bash

watch -d -n 0.2 'ps aux | grep "<defunct>" | grep -v grep | wc -l'
