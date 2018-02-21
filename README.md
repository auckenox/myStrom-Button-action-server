# myStrom-Button-action-server

a small script to use with mystrom buttons or similar buttons that are just calling urls as actions.
the python script opens a webserver on port 8080 (changable in config file) that captures GET requests and uses phue to control a hue bridge. please have a look at the config file (needs to be in the same directory).
i quickly wrote this one for a friend, while it works perfect for her purposes (control hue with mystrom btn) its was written real quick and maybe dirty.

the script uses a yaml config file, where the devices and commands are saved. it features auto-refresh of the config file, if changes to devices in config are detected, it auto reloads it. no need to restart the script.

as device identification string i just used the MAC address of the mystrom button, all capital letters / no „:“ like mystrom do it.

request structure:
`http://[srv-ip]/[MAC-ADDR-in-CAPS-JUST-NUMBERS-AND_A-F]/[eventname]`

request example:
`http://192.168.1.99/5CCF7F0BE2E2/single`

if you need to configure your mystrom button for this here is a quick demo how the code should look:
`curl -v -d "single=get://192.168.4.119:8080/5CCF7F0C2EE6/single&double=get://192.168.4.119:8080/5CCF7F0C2EE6/double&long=get://192.168.4.119:8080/5CCF7F0C2EE6/long&touch=get://192.168.4.119:8080/5CCF7F0C2EE6/touch" http://192.168.4.110/api/v1/device/5CCF7F0C2EE6
`
change ip addresses and MAC according to your needs and send it in a mac/linux like terminal

check their documentation for more infos:
https://mystrom.ch/de/mystrom-for-developers/
