#!/bin/bash

watch -d -n1 'ps aux | grep "<defunct>" | wc -l'
