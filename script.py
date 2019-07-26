# -*- coding: utf-8 -*-
# Needs cec-utils package needs to be installed to use cec-client
import re
import subprocess
import xbmc
import xbmcgui

# The cec-client command can sometimes cause TV to wake from standby, however
# this is fine as we only use it when it should wake if in standby
# TODO: handle command failing
try:
	s = subprocess.check_output('echo pow 0 | cec-client -s -d 1 -m', shell=True)
except:
	xbmc.log("Kodi.Script.TogglePower: cec-client command to get TV status failed")
	quit()
reStatus = re.compile(b'power status: (.+)')
match = re.search(reStatus, s)

if match:
	state = match.group(1)
else:
	state = 'unknown'

if state == 'on':
	xbmc.log("Kodi.Script.TogglePower: Turning off TV with Kodi.Script.TurnOffLGTV")
	xbmc.executebuiltin('RunAddon(kodi.script.turnofflgtv)')
else:
	# Running cec-client has a habit of disabling Kodi's CEC connection,
	# so we can't use its inbuilt CECActivateSource command
	#xbmc.executebuiltin('CECActivateSource')
	xbmc.log("Kodi.Script.TogglePower: Turning on TV with cec-client")
	try:
		subprocess.call('echo on 0 | cec-client -s -d 1 -m', shell=True)
	except:
		xbmc.log("Kodi.Script.TogglePower: cec-client command to turn on TV failed")
