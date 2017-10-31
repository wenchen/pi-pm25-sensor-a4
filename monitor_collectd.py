#!/usr/bin/python

import time
import datetime
import os
import a4
import collectd

PLUGIN_NAME = 'monitor_collectd'
INTERVAL = 300 # seconds
CONFIGS = []

air = a4.a4sensor()
collectd.info('pm25: Loading Python plugin:' + PLUGIN_NAME)

def configure(conf):
    collectd.info('pm25: Configure with: key=%s, children=%r' % (conf.key, conf.children))
    hostname = None
    dev = None

    for node in conf.children:
        key = node.key.lower()
        val = node.values[0]
        if key == 'hostname':
            hostname = val
        elif key == 'dev':
            dev = val
        else:
            collectd.warning('pm25: Unknown config key: %s.' % key)
            continue

    collectd.info("pm25: Configured with hostname %s and device %s" % (hostname, dev))
    CONFIGS.append({'hostname': hostname, 'dev': dev})

def dispatch_value(value, plugin_instance=None, type=None):
    if plugin_instance is None:
        plugin_instance = 'unknown'

    if not type:
        type = 'unknown'

    val = collectd.Values(plugin='pm25')
    val.type = type
    val.plugin_instance = plugin_instance
    val.values = [value]
    val.dispatch()

def get_matrics(conf):
    if not conf['hostname']:
        conf['hostname'] = 'unknown'

    if not conf['dev']:
        collectd.error('Cannot detect your sensor')
        return

    try:
        pmdata = air.read(conf['dev'])
    except:
        pmdata = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    collectd.info('pm25: Reading data (data=%r)' % (pmdata))
    if pmdata[0]:
        dispatch_value(pmdata[0], conf['hostname'], 'pm1')
    if pmdata[1]:
        dispatch_value(pmdata[1], conf['hostname'], 'pm25')
    if pmdata[2]:
        dispatch_value(pmdata[2], conf['hostname'], 'pm10')
    if pmdata[3]:
        dispatch_value(pmdata[3], conf['hostname'], 'um03')
    if pmdata[4]:
        dispatch_value(pmdata[4], conf['hostname'], 'um05')
    if pmdata[5]:
        dispatch_value(pmdata[5], conf['hostname'], 'um10')
    if pmdata[6]:
        dispatch_value(pmdata[6], conf['hostname'], 'um25')
    if pmdata[7]:
        dispatch_value(pmdata[7], conf['hostname'], 'um50')
    if pmdata[8]:
        dispatch_value(pmdata[8], conf['hostname'], 'um100')

def read():
    for conf in CONFIGS:
        get_matrics(conf)

collectd.register_config(configure)
collectd.register_read(read)