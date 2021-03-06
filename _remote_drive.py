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

"""Adapted from PyVisca by Florian Streibelt <pyvisca@f-streibelt.de>"""

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
		self.zoom = 0
		print('[INFO]: CAM Relative Position Class Initialised')

	def update_pos(self):
		return self.ps, self.ts, self.pp, self.tp, self.zoom

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

	data, addr = sock.recvfrom(1024) # initial data for compare
	v.cmd_ptd_home(CAM)
	
	while True:


		newdata, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

		if newdata != data:
			
			v.cmd_ptd_stop(CAM)
			(new_position.CAM, new_position.ps, new_position.ts, new_position.pp, new_position.tp, new_position.zoom) = data.split(' ') 
			(new_position.CAM, new_position.ps, new_position.ts, new_position.pp, new_position.tp, new_position.zoom) = (int(new_position.CAM), int(new_position.ps), int(new_position.ts), int(new_position.pp), int(new_position.tp), int(new_position.zoom))
			v.cmd_ptd_rel(new_position.CAM,new_position.ps,new_position.ts,new_position.pp,new_position.tp)
			
			# zoom based on value passed, it should be a short period, like a button
			if (new_position.zoom == 0):
				v.cmd_cam_zoom_wide(CAM)
			if (new_position.zoom == 2):
				v.cmd_cam_zoom_tele(CAM)
			if (new_position.zoom == 1):
				v.cmd_cam_zoom_stop(CAM)

		# else:	
		# 	print('same')


		data = newdata

		key = cv.waitKey(1) & 0xFF
	
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break


if __name__ == '__main__':
	while True:
		main()