# Licensed under GPLv3, see LICENSE.txt for details
import re
import subprocess
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs

lockdir = 'special://temp/kodi.script.togglepower.inprogress/'

exists = xbmcvfs.exists(lockdir)
if exists:
	xbmc.log('Kodi.Script.ToggleLGTVPower: Not toggling power; lockfile exists', xbmc.LOGINFO)
	# we'll remove the lockdir here, just to avoid the whole functionality seizing up
	# if the dir is created and not destroyed for some reason. it's unlikely that a user
	# will try to power off more than once after initiating power off, and it's better
	# to occasionally fail to detect this than to effectively disable the plugin as
	# something went awry.
	success = xbmcvfs.rmdir(lockdir)
	if not success:
		xbmc.log('Kodi.Script.ToggleLGTVPower: Failed to remove lock directory', xbmc.LOGERROR)
	sys.exit(0)

success = xbmcvfs.mkdir(lockdir)
if not success:
	xbmc.log('Kodi.Script.ToggleLGTVPower: Failed to create lock directory', xbmc.LOGERROR)

d = xbmcgui.DialogProgressBG()
d.create('Power', 'Just a moment while I check whether I need to turn the TV on or off')

xbmc.log("Toggling TV power", xbmc.LOGINFO)

# The cec-client command can sometimes cause TV to wake from standby, however
# this is fine as we only use it when it should wake if in standby
s = subprocess.run('echo pow 0 | ' + bin + ' -s -d 1 -m', shell=True, capture_output=True)
if s.returncode != 0:
	xbmc.log("Kodi.Script.ToggleLGTVPower: cec-client command to get TV status failed, may wake TV anyway", xbmc.LOGERROR)
	xbmc.log(s.stdout.decode(), xbmc.LOGERROR)
	xbmc.log(s.stderr.decode(), xbmc.LOGERROR)
	d.update(100, 'Power', 'Failed to get TV status, may wake TV anyway')
	d.close()
	del d
	success = xbmcvfs.rmdir(lockdir)
	if not success:
		xbmc.log('Kodi.Script.ToggleLGTVPower: Failed to remove lock directory', xbmc.LOGERROR)
	sys.exit(0)

reStatus = re.compile(b'power status: (.+)')
match = re.search(reStatus, s.stdout)

if match:
	state = match.group(1)
else:
	state = 'unknown'

if state == 'on':
	d.update(50, 'Power', 'Turning off TV')
	xbmc.log("Kodi.Script.ToggleLGTVPower: Turning off TV with Kodi.Script.TurnOffLGTV", xbmc.LOGINFO)
	xbmc.executebuiltin('RunAddon(kodi.script.turnofflgtv)', True)
else:
	d.update(50, 'Power', 'Turning on TV')
	xbmc.log("Kodi.Script.ToggleLGTVPower: Turning on TV with cec-client", xbmc.LOGINFO)
	# Running cec-client has a habit of disabling Kodi's CEC connection,
	# so we can't use its inbuilt CECActivateSource command
	#xbmc.executebuiltin('CECActivateSource')
	s = subprocess.run('echo on 0 | ' + bin + ' -s -d 1 -m', shell=True)
	if s.returncode != 0:
		xbmc.log("Kodi.Script.ToggleLGTVPower: cec-client command to turn on TV failed", xbmc.LOGERROR)

d.update(100, 'Done')
d.close()
del d

success = xbmcvfs.rmdir(lockdir)
if not success:
	xbmc.log('Kodi.Script.ToggleLGTVPower: Failed to remove lock directory', xbmc.LOGERROR)
