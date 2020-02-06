def main():
	from pyviscalib.visca import Visca
	from  time import sleep
	v=Visca()


	print ("1")
	CAM=1

	# v.cmd_ptd_reset(CAM)
	# sleep(7)
	# v.cmd_ptd_home(CAM)
	# sleep(2)
	print ("2")
	v.cmd_adress_set()
	print ("3")
	v.cmd_if_clear_all()
	CAM=1
	sleep(1)
	v.cmd_ptd_reset(CAM)
	sleep(7)
	v.cmd_cam_power_on(CAM)
	sleep(2)
	v.cmd_cam_auto_power_off(CAM,0)
	sleep(2)
	v.cmd_datascreen_off(CAM)
	sleep(2)
	v.cmd_ptd_home(CAM)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass


