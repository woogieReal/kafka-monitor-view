#!/bin/bash
set -e

echo 'Waiting for all brokers to join the cluster...'
until kafka-topics.sh --bootstrap-server kafka1:9092 --list > /dev/null 2>&1; do sleep 2; done
until kafka-topics.sh --bootstrap-server kafka2:9092 --list > /dev/null 2>&1; do sleep 2; done
until kafka-topics.sh --bootstrap-server kafka3:9092 --list > /dev/null 2>&1; do sleep 2; done

echo 'All brokers ready. Creating topic...'
kafka-topics.sh --bootstrap-server kafka1:9092 \
  --create --if-not-exists \
  --topic system-metrics \
  --partitions 3 \
  --replication-factor 3

echo 'Topic created.'
kafka-topics.sh --bootstrap-server kafka1:9092 --describe --topic system-metrics
