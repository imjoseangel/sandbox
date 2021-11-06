#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import json
import logging
import os
from os.path import abspath, dirname, normpath
import sys
import pandas as pd
import sqlite3
from config import db
from models import Naming

DATAFILE = 'resourceDefinition.json'
DBFILE = 'resourceDefinition.db'

# Set Logging
logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S", stream=sys.stdout, level=logging.INFO)


# Set local path
local = normpath(abspath(dirname(__file__)))


with open(f'{local}/{DATAFILE}') as resourceDefinition:
    data = json.load(resourceDefinition)

# Create A DataFrame From the JSON Data
df = pd.DataFrame(data)

# Delete database file if it exists currently
if os.path.exists(f'{local}/{DBFILE}'):
    os.remove(f'{local}/{DBFILE}')

# Create the database
db.create_all()

# populate the database
conn = sqlite3.connect(f'{local}/{DBFILE}')
df.to_sql('resourceDefinition', conn, if_exists='append')
