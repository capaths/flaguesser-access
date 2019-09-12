#!/bin/sh

until nc -z ${RABBIT_HOST} ${RABBIT_PORT:5672}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 1
done

echo "Starting service"
nameko run --config config.yaml service
