import os
import errno
import logging

import configparser

DEFAULT_CONFIG = """\
[core]
patrol_home = {PATROL_HOME}
checks_folder = {PATROL_HOME}/checks
log_folder = {PATROL_HOME}/logs
executor = SequentialExecutor
"""

conf = configparser.ConfigParser()

'''
Setting PATROL_HOME and PATROL_CONFIG from environment variables, using
"~/patrol" and "~/patrol/patrol.cfg" as defaults.
'''

if 'PATROL_HOME' not in os.environ:
    PATROL_HOME = os.path.expanduser('~/patrol')
else:
    PATROL_HOME = os.environ['PATROL_HOME']

try:
    os.makedirs(PATROL_HOME)
except OSError as ex:
    if ex.errno == errno.EEXIST and os.path.isdir(PATROL_HOME):
        pass
    else: 
        raise

if 'PATROL_CONFIG' not in os.environ:
    PATROL_CONFIG = PATROL_HOME + '/patrol.cfg'
else:
    PATROL_CONFIG = os.environ['PATROL_CONFIG']

conf = configparser.ConfigParser()
if not os.path.isfile(PATROL_CONFIG):
    '''
    These configuration are used to generate a default configuration when
    it is missing. The right way to change your configuration is to alter your
    configuration file, not this code.
    '''
    logging.info("Createing new config file in: " + PATROL_CONFIG)
    f = open(PATROL_CONFIG, 'w')
    f.write(DEFAULT_CONFIG.format(**locals()))
    f.close()

logging.info("Reading the config from " + PATROL_CONFIG)
conf.read(PATROL_CONFIG)