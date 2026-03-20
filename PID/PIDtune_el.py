import time
import datetime
import rclpy

from necst.core import Commander
from necst import config

rclpy.init()
com = Commander()
com.get_privilege()

time.sleep(1)
com.drive("drive", "on")
com.drive("contactor", "on")
com.record("savespec", save=True)


dist_list = [2]
k_p_list = [2.3]
k_i_list = [0.12]
k_d_list = [0.2]
margin_list = [1.0]
speed_arcsec_list = [1600]

today = str(datetime.date.today()).replace("-", "")

lon = 57
lat = 45


for dist in dist_list:
    for k_p in k_p_list:
        for k_i in k_i_list:
            for k_d in k_d_list:
                for margin in margin_list:
                    for speed_arcsec in speed_arcsec_list:
                        com.pid_parameter("set", Kp=k_p, Ki=k_i, Kd=(k_d), axis="el")
                        com.record(
                            "start",
                            name=f"{today}_test_pid_elscan_kp{k_p}_ki{k_i}_kd{k_d}_speed{speed_arcsec}_lon{lon}_lat{lat}_margin{margin}_range{dist}deg_calc_updated_2ndfix_ratio0.7",
                        )
                        com.antenna(
                            "scan",
                            start=(lon, lat - dist),
                            stop=(lon, lat),
                            scan_frame="altaz",
                            speed=speed_arcsec / 3600,
                            unit="deg",
                            direct_mode=True,
                            margin=margin
                        )

                        time.sleep(3)

                        com.record("stop")

                        time.sleep(5)

com.drive("drive", "off")
com.drive("contactor", "off")
com.record("savespec", save=False)

time.sleep(1)
com.quit_privilege()
com.destroy_node()
rclpy.shutdown()
