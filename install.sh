#!/bin/sh
sudo apt install python3 python3-pip setserial bluez libbluetooth-dev python3-dev
pip install pyserial python-escpos
pip install git+https://github.com/pybluez/pybluez.git#egg=pybluez
sudo mkdir -pv /opt/myristra
sudo cp * /opt/myristra
sudo chown -R nobody /opt/myristra
cp Myristra.desktop $HOME/Desktop
sudo cp Myristra.desktop /usr/share/applications
cp Myristra.desktop $HOME/.config/autostart