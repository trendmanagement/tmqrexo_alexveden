"""
Standalone bulk EXO quotes updater

Can be used to backfill EXO quotes or populate new EXOs with data

EXO start date: 2011-06-01
"""
# import modules used here -- sys is a very standard one
import sys, argparse, logging
import os
from scripts.settings_exo import INSTRUMENTS_LIST

try:
    from .settings import *
except SystemError:
    from scripts.settings import *

try:
    from .settings_local import *
except SystemError:
    try:
        from scripts.settings_local import *
    except ImportError:
        pass
    pass


for instrument in INSTRUMENTS_LIST:
    os.system('python3.5 ./exo_builder.py --logfile=./logs/exo/exo_batch_build_{0}.log -B 2011-06-01 {0}'.format(instrument))