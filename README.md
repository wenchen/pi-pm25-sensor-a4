# CP-15-A4-CG
Read Partitle Matter (PM) data with [A4 Sensor](https://www.aliexpress.com/store/product/Laser-PM2-5-particle-mass-concentration-sensor-A4-dust-dust-sensors-INSAN-CP-15-A4/1725971_32637917424.html).
Added ability to intergrate with [InfluxDB](https://github.com/influxdata/influxdb) by using [collectd](https://github.com/collectd/collectd).

# Installation

## Prerequisites
- Python 2
- [pyserial](https://github.com/pyserial/pyserial), `pip install pyserial`

## Quick Start

1. Obtain the location of serial device (e.g. `/dev/ttyUSB0`)
2. Update the last line of `a4.py` with that location

```python
    print air.read("/dev/ttyAMA0") // update device
```

3. Test run

```
python a4.py
```

## Intergrate with InfluxDB and collectd

1. Install Collectd & influxDB

```
sudo apt install collectd influxdb
```

2. Edit /etc/influxdb/influxdb.conf with following content:

```
[[collectd]]
  enabled = true
  bind-address = ":25827"
  database = "pm25_db"
  typesdb = "/etc/influxdb/pm25/"
```

3.

```
mkdir -p /etc/influxdb/pm25
cp types.db /etc/influxdb/pm25
ln -s /etc/influxdb/pm25/types.db /usr/share/collectd/types.db
```

4. Change /etc/collectd.conf with following content

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

5. Restart collectd and Influxdb
```
sudo systemctl restart collectd
sudo systemctl restart influxdb
```

NOTE: While using Grafana, one may import dashboard from `pm2.5.json`

# Usage

python a4.py
[21, 32, 31, 947, 1963, 5959, 35, 0, 0]

[pm1, pm10, pm2.5, 0.3um, 0.5um, 1.0um, 2.5um, 5.0um, 10um]

# Notes
- Remember to remove any serial console related configurations from `cmdline.txt`
- To stop any messages like `sysrq: Sysrq : HELP : .....`: `echo 0 > /proc/sys/kernal/sysrq`
