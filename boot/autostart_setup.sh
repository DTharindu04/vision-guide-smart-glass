#!/usr/bin/env bash
set -e
sudo cp boot/smartglasses.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable smartglasses.service
sudo systemctl restart smartglasses.service
sudo systemctl status smartglasses.service --no-pager
