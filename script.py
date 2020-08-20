# Licensed under GPLv3, see LICENSE.txt for details
import re
import subprocess
import xbmc
import xbmcgui

d = xbmcgui.DialogProgressBG()
d.create('POWER', 'Just a moment while I check whether I need to turn the TV on or off')

xbmc.log("Toggling TV power", xbmc.LOGNOTICE)

# The cec-client command can sometimes cause TV to wake from standby, however
# this is fine as we only use it when it should wake if in standby
try:
	s = subprocess.check_output('echo pow 0 | cec-client -s -d 1 -m', shell=True)
except:
	xbmc.log("Kodi.Script.ToggleLGTVPower: cec-client command to get TV status failed, may wake TV anyway", xbmc.LOGERROR)
	d.update(100, 'Failed to get TV status, may wake TV anyway')
	d.close()
	quit()
reStatus = re.compile(b'power status: (.+)')
match = re.search(reStatus, s)

if match:
	state = match.group(1)
else:
	state = 'unknown'

if state == 'on':
	d.update(50, 'Turning off TV')
	xbmc.log("Kodi.Script.ToggleLGTVPower: Turning off TV with Kodi.Script.TurnOffLGTV", xbmc.LOGNOTICE)
	xbmc.executebuiltin('RunAddon(kodi.script.turnofflgtv)')
else:
	d.update(50, 'Turning on TV')
	xbmc.log("Kodi.Script.ToggleLGTVPower: Turning on TV with cec-client", xbmc.LOGNOTICE)
	# Running cec-client has a habit of disabling Kodi's CEC connection,
	# so we can't use its inbuilt CECActivateSource command
	#xbmc.executebuiltin('CECActivateSource')
	try:
		subprocess.call('echo on 0 | cec-client -s -d 1 -m', shell=True)
	except:
		xbmc.log("Kodi.Script.ToggleLGTVPower: cec-client command to turn on TV failed", xbmc.LOGERROR)

d.update(100, 'Done')
d.close()
