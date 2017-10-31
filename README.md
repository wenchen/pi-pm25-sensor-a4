# CP-15-A4-CG
read pm data from a4 sensor with python

# install and run

download a4.py and install python modules

    apt-get install python-pip python-serial

check your tty device (ttyUSB0 or ttyAMA0)
update a4.py last line
    
    print air.read("/dev/ttyAMA0") // update device

give a try

    python a4.py

# Intergrate with influxDB and collectd
1. Install Collectd & influxDB
```
sudo apt install collectd influxdb
```

2. edit /etc/influxdb/influxdb.conf add the following config
```
[[collectd]]
  enabled = true
  bind-address = ":25827"
  database = "pm25_db"
  typesdb = "/etc/influxdb/pm25/"
```

3. create /etc/influxdb/pm25 and copy types.db to this place

4. copy types.db to /usr/share/collectd/

5. edit /etc/collectd.conf and add the following config
```
LoadPlugin network
LoadPlugin python
<Plugin network>
    Server "127.0.0.1" "25827"
    Forward true
</Plugin>
<Plugin python>
    ModulePath "/home/pi/pi-pm25-sensor-a4"
    LogTraces true
    Interactive false
    Import "monitor_collectd"
    <Module monitor_collectd>
        hostname "room-3f"
        dev "/dev/ttyAMA0"
    </Module>
</Plugin>
```

6. restart collectd and influxdb
```
sudo systemctl restart collectd
sudo systemctl restart influxdb
```

7. If you use Grafana, you can import dashboard file pm2.5.json

# Output

python a4.py
[21, 32, 31, 947, 1963, 5959, 35, 0, 0]

[pm1, pm10, pm2.5, 0.3um, 0.5um, 1.0um, 2.5um, 5.0um, 10um]

# Warning
    remove serial console ralated config from cmdline.txt

# to stop  sysrq: SysRq : HELP : ...... messag
    echo 0 > /proc/sys/kernel/sysrq
