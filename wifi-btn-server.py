#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
############### REQUIRED ###############
pip install pyyaml phue requests
"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os,re,yaml,json,logging,logging.handlers,time,hashlib,requests
from phue import Bridge

scversion = "1.0"

def readConfig():
  try:
    with open("wifi-btn-server.yml", 'r') as ymlfile:
      cfgx = yaml.load(ymlfile)
      return cfgx
  except Exception as e:
    print e

cfg = readConfig()
server_port = cfg['server']['port']
srv_name = cfg['server']['name']


print "\n\n------------------------------------------------------------------"
print "Version %s" %scversion, " starting up .."
print "Server Name: %s" %srv_name
print "Webserver running on port %i"%server_port
print "------------------------------------------------------------------\n\n"

############ LOGGING #########################################################
logging.basicConfig()
my_logger = logging.getLogger(srv_name)
my_logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address = ('192.168.4.200',514))
my_logger.addHandler(handler)
my_logger.info("wifi-btn-server v%s starting up.."%scversion)

############ HUE BRIDGE #######################################################
try:
  b = Bridge(cfg['server']['hue_bridge_config']['address'])
  b.connect()
  b.get_api()
  print "hue bridge found and connected"
except Exception as e:
  print "warning, hue failed to connect: %s" %e

############ FUNCTIONS ########################################################
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

configMD5=md5('wifi-btn-server.yml')

def acUrlRequest(btnCFG):
  print "getting url %s" %btnCFG['url']
  try:
    r = requests.get(btnCFG['url'],timeout=3)
    print r.text
  except Exception as e:
    print "could not get url: %s" %e

def acHueRequest(btnCFG):
  global b
  if btnCFG['type'] == "set_scene":
    b.run_scene(btnCFG['group'], btnCFG['scene'])
    print "set scene %s on group %s" %(btnCFG['scene'], btnCFG['group'])
    return True
  print "hue action type not found: %s" %btnCFG['type']
  
def getButtonInfos(ip,mac):
  url = "http://%s/api/v1/device/%s" %(ip,mac)
  r = requests.get(url,timeout=3.5)
  print r.text


############ HTTP SERVER ########################################################
class auckenox_RQH(BaseHTTPRequestHandler):
  
  def log_message(self, format, *args):
    return False

  def do_OPTIONS(self):
    self.sendResponse(200)

  def do_GET(self):
    matchi = False
    global configMD5
    global cfg
    btn_IP = self.client_address[0]

    # reload config if changed
    if configMD5 != md5('wifi-btn-server.yml'):
      print "reloading config.."
      cfg = readConfig()
      configMD5 = md5('wifi-btn-server.yml')

    
    p = re.compile(ur'\/([0-9A-F]*)\/(single|double|long|touch)') 
    match = re.search(p, self.path)
    if match != None:
      matchi = True
      btn_mac = match.group(1)
      btn_act = match.group(2)
      print "button %s, has action %s for me" %(btn_mac,btn_act)

      try:
          btnCFG = cfg[btn_mac][btn_act]

          if btnCFG['action'] == "url":
            acUrlRequest(btnCFG)
          elif btnCFG['action'] == "hue":
            acHueRequest(btnCFG)
          elif btnCFG['action'] == "fooo":
            print "fooo"
          else:
            print "action: %s is not available, please use hue or url" %btn_act

      except Exception as e:
        print "this is error man: %s" %e
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.end_headers()
        self.wfile.write('there was a error: %s'%e)
      
    if not matchi:
      print "no matches for request"
      self.send_response(404)
      self.send_header('Content-type','text/html')
      self.send_header('Access-Control-Allow-Origin', '*')
      self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
      self.end_headers()

def run():
  server_address = ('', server_port)
  httpd = HTTPServer(server_address, auckenox_RQH)
  httpd.serve_forever()
  
if __name__ == '__main__':
  run()
