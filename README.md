# pms3003-g3
read pm data from pms3003 g3 sensor with python

# install and run

download g3.py and install python modules

    apt-get install python-pip python-serial

check your tty device (ttyUSB0 or ttyAMA0)
update g3.py last line
    
    print air.read("/dev/ttyAMA0") // update device

give a try

    python g3.py

# Output

python g3.py
[2, 8, 5, 2, 8, 5]

[pm1_cf, pm10_cf, pm2.5_cf, pm1, pm10, pm2.5]

First three data (pmX_cf, cf=1) is the to value is a TSI For standard data.

Last three is reading to the value of value is an atmosphere as the standard.

# to stop  sysrq: SysRq : HELP : ...... messag
    echo 0 > /proc/sys/kernel/sysrq
