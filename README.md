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

# to stop  sysrq: SysRq : HELP : ...... messag
    echo 0 > /proc/sys/kernel/sysrq
