#!/usr/bin/env python3

import os
import subprocess
import sys
import re
API_KEY = '586a06a5fdd519aef29b0774a857168d4c4fee38a96917326d7cca3e85c21b81'
TARGET = sys.argv[1]
PACKAGE = subprocess.check_output('adb shell pm list packages | grep ' + TARGET, shell=True)
PACKAGE_NAME = re.sub(r'.*package:', '', PACKAGE.decode())
PATH = re.sub(r'.*package:', '', subprocess.check_output('adb shell pm path ' + PACKAGE_NAME, shell=True).decode())
APK = re.sub(r'.*package:', '', subprocess.check_output('adb shell pm path ' + PACKAGE_NAME, shell=True).decode()).rsplit('/', 1)[-1]
#os.system('adb pull ' + PATH)
#RENAME = "mv " + APK.rstrip() + " " + TARGET + ".apk"
#os.system(str(RENAME))
APK_PATH = subprocess.check_output('pwd', shell=True).decode().strip()
UPLOAD_FILE = "curl -F 'file=@%s/%s.apk' http://localhost:8000/api/v1/upload -H 'Authorization:'%s" % (APK_PATH, TARGET, API_KEY)
UPLOAD_RESPONSE  = str(UPLOAD_FILE)
UPLOAD_HASH = re.sub(r'"','',re.sub(r', "file_name"', '', os.popen(UPLOAD_FILE).read()).rsplit(': ', 2)[1])

print(UPLOAD_HASH)

