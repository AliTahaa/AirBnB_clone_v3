#!/usr/bin/python3
import sys
import shutil
import subprocess
import os

"""
 Test if db test and db_storage are present
"""
if not os.path.exists("tests/test_models/test_engine/test_db_storage.py"):
    print("No db")
    exit(1)
if not os.path.exists("models/engine/db_storage.py"):
    print("No db")
    exit(1)

"""
 Restore
"""
try:
    shutil.copy("models/engine/tmp_db_storage.py", "models/engine/db_storage.py")
except Exception as e:
    print(e)
try:
    shutil.copy("models/engine/tmp__init__.py", "models/engine/__init__.py")
except Exception as e:
    print(e)

"""
 Backup
"""
try:
    shutil.copy("models/engine/db_storage.py", "models/engine/tmp_db_storage.py")
except Exception as e:
    print(e)

"""
 get fake and move to correct folder
"""
fake_storage_db_name = sys.argv[1]
try:
    shutil.copy(fake_storage_db_name, "models/engine/db_storage.py")
except Exception as e:
    print(e)

"""
 Run test
"""
process = subprocess.Popen(["python3", "-m", "unittest", "tests/test_models/test_engine/test_db_storage.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()
s_total = "{}{}".format(output, error)

if "FAIL" in s_total or "Traceback" in s_total:
    print("OK", end="")


"""
 Restore
"""
try:
    shutil.copy("models/engine/tmp_db_storage.py", "models/engine/db_storage.py")
except Exception as e:
    pass
