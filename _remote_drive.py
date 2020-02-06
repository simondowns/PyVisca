#! /usr/bin/env python
# -*- coding: utf8 -*-
#
#    PyVisca - Implementation of the Visca serial protocol in python
#    Copyright (C) 2013  Florian Streibelt pyvisca@f-streibelt.de
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 2 only.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#    USA

"""PyVisca by Florian Streibelt <pyvisca@f-streibelt.de>"""

#
# This is used for testing the functionality while developing,
# expect spaghetti code...
#

import subprocess as sp
import socket
import cv2 as cv

class CAM_position():

	def __init__(self, CAM):
		self.CAM = CAM
		self.ps = 10
		self.ts = 10
		self.pp = 0
		self.tp = 0
		print('[INFO]: CAM Relative Position Class Initialised')

	def update_pos(self):
		return self.ps, self.ts, self.pp, self.tp

def main():
	from pyviscalib.visca import Visca
	from  time import sleep

	v=Visca()
	CAM=1
	new_position = CAM_position(CAM)

	UDP_IP = "127.0.0.1"
	UDP_PORT = 5005

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))



	while True:


		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		# print ("received message:", data)

		

		(new_position.CAM, new_position.ps, new_position.ts, new_position.pp, new_position.tp) = data.split(' ') 
		(new_position.CAM, new_position.ps, new_position.ts, new_position.pp, new_position.tp) = (int(new_position.CAM), int(new_position.ps), int(new_position.ts), int(new_position.pp), int(new_position.tp))
		#print(new_position.CAM,new_position.ps,new_position.ts,new_position.pp,new_position.tp)
		v.cmd_ptd_rel(new_position.CAM,new_position.ps,new_position.ts,new_position.pp,new_position.tp)

		# raw_pos = pospipe.stdout.read()

		# # new_position = pospipe.stdout.read(CAM_POS)

		# # v.cmd_ptd_rel(new_position.CAM,new_position.ps,new_position.ts,new_position.pp,new_position.tp)

		key = cv.waitKey(1) & 0xFF
	
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	# v.cmd_ptd_home(CAM)
	# sleep(2)
	# v.cmd_ptd_reset(CAM)

	# v.cmd_cam_power_off(CAM)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass


