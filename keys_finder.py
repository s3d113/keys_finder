#!/usr/bin/env python3
from pwn import *
import os
import subprocess
import sys
import re

sys.stderr = os.devnull
TARGET = sys.argv[1]
PACKAGE = subprocess.check_output('adb shell pm list packages | grep ' + TARGET +' | head -n 1', shell=True)
text = str(PACKAGE, 'utf-8')
package_name = log.progress("Getting Package: "+ text)
package_name.status("On it .....")
time.sleep(1)
package_name.success("Pacakge found !")
PACKAGE_NAME = re.sub(r'.*package:', '', PACKAGE.decode()).strip()
PATH = re.sub(r'.*package:', '', subprocess.check_output('adb shell pm path ' + PACKAGE_NAME +' | head -n 1', shell=True).decode()).strip()
log.info("Path is: "+ PATH)
APK = re.sub(r'.*package:', '', subprocess.check_output('adb shell pm path ' + PACKAGE_NAME + ' | head -n 1', shell=True).decode()).rsplit('/', 1)[-1]
os.system('adb pull ' + PATH + ' >/dev/null')
pull = log.progress("Pulling: " + APK)
pull.status("On it.....")
time.sleep(1)
pull.success("Package pulled!")
RENAME = "mv " + APK.rstrip() + " " + TARGET + ".apk"
os.system(str(RENAME))
log.success('Renamed the Package to: ' + TARGET + '.apk')
#RUN = subprocess.Popen('/usr/bin/apktool d ' + TARGET + '.apk', stderr=subprocess.PIPE)
#RUN.communicate()
os.system('/usr/bin/apktool d ' + TARGET +'.apk'+ ' >/dev/null')
dump = log.progress("Decompiling code ....")
dump.status("On it .....")
time.sleep(3)
dump.success("Done!")
APK_PATH = subprocess.check_output('pwd', shell=True).decode().strip()
KEY_GREP = "cat " + APK_PATH + "/" + TARGET + "/res/values/strings.xml  | egrep -i  '_key|api_|key_|_api' | sed 's!<string name=\"!!g' | sed 's!</string>!!g' | sed 's!\">!: !g'"
log.success("Keys Found: ")
os.system(KEY_GREP)
