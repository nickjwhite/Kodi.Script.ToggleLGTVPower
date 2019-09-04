# Licensed under GPLv3, see LICENSE.txt for details
import re
import subprocess
import xbmc

xbmc.log("Toggling TV power", xbmc.LOGNOTICE)

# The cec-client command can sometimes cause TV to wake from standby, however
# this is fine as we only use it when it should wake if in standby
try:
	s = subprocess.check_output('echo pow 0 | cec-client -s -d 1 -m', shell=True)
except:
	xbmc.log("Kodi.Script.TogglePower: cec-client command to get TV status failed, may wake TV anyway", xbmc.LOGERROR)
	quit()
reStatus = re.compile(b'power status: (.+)')
match = re.search(reStatus, s)

if match:
	state = match.group(1)
else:
	state = 'unknown'

if state == 'on':
	xbmc.log("Kodi.Script.TogglePower: Turning off TV with Kodi.Script.TurnOffLGTV", xbmc.LOGNOTICE)
	xbmc.executebuiltin('RunAddon(kodi.script.turnofflgtv)')
else:
	xbmc.log("Kodi.Script.TogglePower: Turning on TV with cec-client", xbmc.LOGNOTICE)
	# Running cec-client has a habit of disabling Kodi's CEC connection,
	# so we can't use its inbuilt CECActivateSource command
	#xbmc.executebuiltin('CECActivateSource')
	try:
		subprocess.call('echo on 0 | cec-client -s -d 1 -m', shell=True)
	except:
		xbmc.log("Kodi.Script.TogglePower: cec-client command to turn on TV failed", xbmc.LOGERROR)
