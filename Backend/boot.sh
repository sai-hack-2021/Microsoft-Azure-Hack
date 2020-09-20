#!/bin/bash


if [ "$BOOT" = "TRUE" ]; then
    echo "The boot value is $BOOT"
    python3 boot.py
    cd src/

    gunicorn -b 0.0.0.0:8000 src.app

else

    cd src/

    gunicorn -b 0.0.0.0:8000 src.app

fi



