import shutil

try:
    shutil.rmtree('jobs')
except:
    pass
try:
    shutil.rmtree('tasks')
except:
    pass

import os

os.remove("triggers.json")
os.remove("jobs.json")