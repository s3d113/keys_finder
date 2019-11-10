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
os.system('adb pull ' + PATH)
RENAME = "mv " + APK.rstrip() + " " + TARGET + ".apk"
os.system(str(RENAME))
APK_PATH = subprocess.check_output('pwd', shell=True).decode().strip()
UPLOAD_FILE = "curl -s -F 'file=@%s/%s.apk' http://localhost:8000/api/v1/upload -H 'Authorization:'%s" % (APK_PATH, TARGET, API_KEY)
UPLOAD_RESPONSE  = str(UPLOAD_FILE)
UPLOAD_HASH = re.sub(r'"','',re.sub(r', "file_name"', '', os.popen(UPLOAD_FILE).read()).rsplit(': ', 2)[1])
SCAN = "curl -X POST  -s --output /dev/null --url http://localhost:8000/api/v1/scan --data 'scan_type=apk&file_name=%s.apk&hash=%s' -H 'Authorization:%s'" % (TARGET, UPLOAD_HASH, API_KEY)
os.system(SCAN)
KEY_GREP = "curl -is -X POST --url http://localhost:8000/api/v1/report_json --data 'hash=%s&scan_type=apk' -H 'Authorization:%s'  | grep -o -i -P '.{0,13}_key.{0,45}' | awk '{print $1, $3}' | tr -d '\\' 2> /dev/null | tr -d '\"' 2> /dev/null | tr -d ',' 2> /dev/null" % (UPLOAD_HASH, API_KEY)
os.system(KEY_GREP)
