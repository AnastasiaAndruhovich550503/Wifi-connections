import os
import time

class WifiFinder:

    """Collects info about connected devices"""

    def get_wifi_connections(self):
        os.system("iwlist wlp3s0 scanning | egrep 'Address|ESSID|Quality|Authentication Suites' > output")

    def get_wifi_table(self):
        output = open("output")
        wifi_list = list()
        output_lines = output.readlines()
        password_flag = True
        for line in output_lines:
            if line.find("Address") != -1:
                if not password_flag:
                    wifi_list.append(" ".join('-'))
                wifi_list.append(" ".join(line.split()[4:]))
                password_flag = False
            if line.find("ESSID") != -1:
                string = " ".join(line.split('"')[1:])
                wifi_list.append(" ".join(string.split('\n')))
            if line.find("Quality") != -1:
                string = " ".join(line.split('=')[1:])
                wifi_list.append(" ".join(string.split()[:1]))
            if line.find("Authentication Suites") != -1:
                wifi_list.append(" ".join(line.split()[4:]))
                password_flag = True
        return wifi_list



