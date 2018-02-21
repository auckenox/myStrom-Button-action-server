# myStrom-Button-action-server

a small script to use with mystrom buttons or similar buttons that are just calling urls as actions.
the python script opens a webserver on port 8080 (changable in config file) that captures GET requests and uses phue to control a hue bridge. please have a look at the config file (needs to be in the same directory).
i quickly wrote this one for a friend, while it works perfect for her purposes (control hue with mystrom btn) its was written real quick and maybe dirty.

the script uses a yaml config file, where the devices and commands are saved. it features auto-refresh of the config file, if changes to devices in config are detected, it auto reloads it. no need to restart the script.

request structure:
`http://[srv-ip]/[MAC-ADDR-in-CAPS-JUST-NUMBERS-AND_A-F]/[eventname]`

request example:
`http://192.168.1.99/5CCF7F0BE2E2/single`


