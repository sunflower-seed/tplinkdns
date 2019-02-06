#!/usr/bin/env python3

import sys
import ipaddress
from selenium import webdriver

# DNS update script for TP-Link Archer VR600v Router
#
# Sadly the TP-Link Archer VR600v does not provide remote access despite a telnet shell.
# Therefore it is not possible to change DNS Server values on the fly.
# Additionally the GUI is heavy JS loaded with security features,
# which makes it difficult to access any maybe existing API.
#
# This scripts makes use of selenium webdriver to simply manipulate the router GUI.
# It might be suitable for other use cases.
#
# usage: tplinkdns.py [NEW_IP] 
#
# author: Phil <development@beph.de>
#
# version: 1.0

dnsnew_ip = sys.argv[1]

# URL of router in LAN
routerurl = '192.168.1.1'
# Password to router GUI
routerpassword = 'CHANGE ME!'

#verify IP input
ipaddress.ip_address(dnsnew_ip)

# Configure Webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

# set the window size (router GUI has about 1000 x 1400 px)
options.add_argument('window-size=1024x1600')

# initialize the driver
driver = webdriver.Chrome(chrome_options=options)

try:

  # Connect to Router

   driver.get('https://' + routerurl)
   driver.implicitly_wait(2)

   # Login

   password = driver.find_element_by_css_selector('input[type=password]')
   login = driver.find_element_by_css_selector('#pc-login-btn')

   password.send_keys(routerpassword)
   login.click()

   driver.implicitly_wait(2)

   # Check if someone is already logged in and force logout

   try:
      alert = driver.find_element_by_css_selector('#alert-container #confirm-yes')
      alert.click()
   except Exception:
      pass

   driver.implicitly_wait(2)

   # Open DNS Settings

   advanced = driver.find_element_by_css_selector('li#advanced')
   advanced.click()
   driver.implicitly_wait(1)
   network = driver.find_element_by_css_selector('a[url="wan.htm"]')
   network.click()
   dhcp = driver.find_element_by_css_selector('a[url="dhcp.htm"]')
   dhcp.click()

   # Set new DNS

   dns1_ip = driver.find_elements_by_css_selector('input.dnsserver1-address-cell')
   dnsnew_ip = dnsnew_ip.split('.')

   assert len(dns1_ip) == 4
   assert len(dnsnew_ip) == 4

   for dns1_ip_subset, dnsnew_ip_subset in zip(dns1_ip, dnsnew_ip):
       dns1_ip_subset.clear()
       dns1_ip_subset.send_keys(dnsnew_ip_subset)

   save = driver.find_element_by_css_selector('#saveIPv4Ng')
   save.click()

   driver.implicitly_wait(2)

   # Logout

   logout = driver.find_element_by_css_selector('a#topLogout')
   logout.click()

   logout_msg = driver.find_element_by_css_selector('#alert-container .btn-msg-ok')
   logout_msg.click()

   # Make shure logout is performed
   driver.implicitly_wait(3)

# Close webdriver in every case otherwise browser is not terminated

finally:
   driver.quit()
