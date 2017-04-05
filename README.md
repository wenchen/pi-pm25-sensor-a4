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

# Output

python a4.py
[21, 32, 31, 947, 1963, 5959, 35, 0, 0]

[pm1, pm10, pm2.5, 0.3um, 0.5um, 1.0um, 2.5um, 5.0um, 10um]

# to stop  sysrq: SysRq : HELP : ...... messag
    echo 0 > /proc/sys/kernel/sysrq
