import os
import sys
import errno
import logging
from time import strftime
import configparser

# Setting default config and reading config file (if exists)

DEFAULT_CONFIG = """\
[core]
patrol_home = {PATROL_HOME}
checks_folder = {PATROL_HOME}/checks
reports_folder = {PATROL_HOME}/reports
log_folder = {PATROL_HOME}/logs
executor = SequentialExecutor
patrol_conn = sqlite:///{PATROL_HOME}/patrol.db
"""

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


# Setting up logging

log_dir = conf.get('core', 'LOG_FOLDER')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = '{}/app_{}.log'.format(log_dir, strftime('%Y-%m-%d'))
log_format =  \
    "[%(asctime)s] %(levelname)s - %(message)s  [%(name)s %(pathname)s %(lineno)d]"

logging.basicConfig(
    filename=log_file, level=logging.INFO, format=log_format, force=True)

# Set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# Set format which better fits console
formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s: %(message)s', "%H:%M:%S")
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logging.info("Logging into: " + log_file)

#Creating a handler for unhandled exceptions
def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Will call default excepthook
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    #Create a critical level log message with info from the except hook.
    logging.critical("Unhandled exception: ", exc_info=(exc_type, exc_value, exc_traceback))

# Assign the excepthook to the handler
sys.excepthook = handle_unhandled_exception
