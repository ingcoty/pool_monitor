from OTA_Updater import OTA_Updater
from wifi_config import SSID, PASSWORD
import urequests
import json
import machine


class OTA_Wrapper:

    def __init__(self, github_url: str):
        self.github_url = "https://raw.githubusercontent.com/ingcoty/tank_mmonitor/master/"
        self.headers = {"accept": "application/json"} 
        exceptions = [".github/workflows"]
        try:
            resp = urequests.get(github_url, headers=self.headers)
            if resp.status_code == 200:
                data = json.loads(resp.text)
                files = [file["name"] for file in data["payload"]["tree"]["items"] if file["name"] not in exceptions]
                for file in files:
                    ota = OTA_Updater(ssid=SSID, password=PASSWORD, repo_url=self.github_url, filename=file)
                    ota.download_and_install_update_if_available()
        except:
            print("!Error getting github files...")


