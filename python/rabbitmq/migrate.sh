#!/bin/bash


jq 'del ( .parameters, .policies, .global_parameters, .vhosts, .product_version, .product_name, .rabbitmq_version, .rabbit_version)' definitions.json

rabbitmqctl set_parameter federation-upstream blue '{"uri":"amqp://node-in-blue-cluster"}'
rabbitmqctl set_policy --apply-to queues blue-green-migration ".*" '{"federation-upstream-set":"all"}'

rabbitmqctl set_parameter shovel drain-blue '{"src-protocol": "amqp091", "src-uri": "amqp://user:password@blueip", "src-queue": "queue1", "dest-protocol": "amqp091", "dest-uri": "amqp://user:password@rabbitmq.rabbitmq.svc.cluster.local", "dest-queue": "queue1"}'

kubectl exec -n rabbitmq rabbitmq-release-0 -- rabbitmqctl export_definitions - | jq 'del ( .parameters, .policies, .global_parameters, .vhosts, .product_version, .product_name, .rabbitmq_version, .rabbit_version)'
kubectl exec -n rabbitmq rabbitmq-server-0 -- rabbitmqctl import_definitions

kubectl exec -n rabbitmq rabbitmq-release-0 -- rabbitmqctl export_definitions - | jq 'del ( .parameters, .policies, .global_parameters, .vhosts, .product_version, .product_name, .rabbitmq_version, .rabbit_version) .queues[].name'

curl -u {username}:{password} -X GET http://{hostname}:15672/api/definitions | jq 'del ( .parameters, .policies, .global_parameters, .vhosts, .product_version, .product_name, .rabbitmq_version, .rabbit_version)' | curl -u {username}:{password} -X POST http://{hostname}:15672/api/definitions
