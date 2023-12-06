__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2023, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "beta"
__maintainer__ = "Florian Thiery"
__email__ = "florian.thiery@leiza.de"
__status__ = "beta"
__update__ = "2023-12-06"

# import dependencies
import uuid
import shortuuid
import requests
import io
import pandas as pd
import os
import codecs
import datetime
import importlib
import sys
import hashlib
from pathlib import Path  # for file management

# https://pypi.org/project/shortuuid/

importlib.reload(sys)

# paths

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_project_root() -> Path:
    return Path(__file__).parent.parent


Path = get_project_root()

# set starttime
lines = []

# create UUIDs

lines.append("row" + "," + "id" + "," + "uuid")
i = 1
while i <= 42000:
    code = str(i) + "AE-AD"
    u = shortuuid.uuid(name=code)
    lines.append(str(i) + "," + u + "," + "AE-AD_" + u)
    i = i + 1

# write output files

filename = Path.joinpath("uuid").joinpath("uuids-AEAD.csv")
file = codecs.open(filename, "w", "utf-8")
for i, line in enumerate(lines):
    file.write(line)
    file.write("\r\n")
file.close()

print("*****************************************")
print("SUCCESS: closing script")
print("*****************************************")
