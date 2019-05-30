#!/usr/local/bin/bash

CONFIG_FILE=/my/folder/config.yaml

docker -H :4000 run -d -v ${CONFIG_FILE}:/config.yaml signiant/azure-team-cost-reporter -c /config.yaml
