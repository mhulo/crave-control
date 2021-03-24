#!/bin/bash

sudo cp crave.service /etc/systemd/system/crave.service
sudo systemctl enable crave.service
sudo systemctl start crave.service
