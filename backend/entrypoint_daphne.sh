#!/bin/bash

exec daphne -b 0.0.0.0 -p 8001 events.asgi:application