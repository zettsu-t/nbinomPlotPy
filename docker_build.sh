#!/bin/bash
docker-compose build --build-arg "$(< password_digest.txt)"
