# Kodi TogglePower script

This addon gets the current power status of the TV using CEC, and turns
it off if it is on, or on if it is off. It uses CEC to turn the TV on,
and the Kodi.Script.TurnOffLGTV script to turn the TV off.

The Kodi.Script.TurnOffLGTV script can be found at
https://github.com/BillyNate/Kodi.Script.TurnOffLGTV

This addon requires the cec-utils package to be installed.

This addon uses cec-client, rather than Kodi's inbuilt CEC functions.
This is because Kodi offers no way to determine the status of a CEC
device. Running cec-client tends to disable Kodi's CEC connection,
so this addon does everything with cec-client instead.
