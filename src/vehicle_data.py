import requests
import time

MAIN_URL = "https://moj.gov.pl/nforms/engine/ng/index?xFormsAppName=HistoriaPojazdu"
DATA_URL = "https://moj.gov.pl/nforms/api/HistoriaPojazdu/1.0.18/data/vehicle-data"

def build_session_value():
    app_name = "HistoriaPojazdu"
    timestamp = int(time.time() * 1000)  
    return f"{app_name}:{timestamp}"

class VehicleDataFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://gov.pl",
            "Referer": "https://moj.gov.pl/nforms/engine/ng/index?xFormsAppName=HistoriaPojazdu"
        })
        self.nf_wid_value = build_session_value()
        self.initialize_session()

    def initialize_session(self):
        form_data = {
            "NF_WID": self.nf_wid_value,
            "varKey": "NF_WID",
            "varApplicationName": "HistoriaPojazdu"
        }
        self.session.post(MAIN_URL, data=form_data, timeout=10)
        self.xsrf_token = self.session.cookies.get('XSRF-TOKEN')

    def get_vehicle_data(self, registration_number, vin_number, first_registration_date, timeout=15):
        payload = {
            "registrationNumber": registration_number,
            "VINNumber": vin_number, 
            "firstRegistrationDate": first_registration_date
        }
        
        headers = {
            "NF_WID": self.nf_wid_value,
            "X-XSRF-TOKEN": self.xsrf_token
        }
        
        return self.session.post(DATA_URL, json=payload, headers=headers, timeout=timeout)