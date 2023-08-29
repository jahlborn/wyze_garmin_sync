import math
import os
import sys
import wyze_sdk
import logging
#logging.basicConfig(level=logging.DEBUG)
from fit import FitEncoder_Weight
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError
from datetime import datetime, timedelta
from wyze_sdk.models import (JsonObject, PropDef, epoch_to_datetime,
                             show_unknown_key_warning)
from wyze_sdk.models.devices import AbstractWirelessNetworkedDevice, DeviceProp
from wyze_sdk.api.base import BaseClient
from wyze_sdk.errors import WyzeRequestError
from wyze_sdk.models.devices import DeviceModels, Scale, ScaleRecord, UserGoalWeight
from wyze_sdk.service import WyzeResponse

response = Client().login(email=os.environ['WYZE_EMAIL'], password=os.environ['WYZE_PASSWORD'], key_id=os.environ['WYZE_KEY_ID'],api_key=os.environ['WYZE_API_KEY'])
#print(f"access token: {response['access_token']}")
#print(f"refresh token: {response['refresh_token']}")
os.environ['WYZE_ACCESS_TOKEN'] = ', '.join({response['access_token']})


def write_scale_data(record, fname):
    fit = FitEncoder_Weight()
    fit.write_file_info(time_created=math.trunc(record.measure_ts / 1000))
    fit.write_file_creator()
    fit.write_device_info(timestamp=math.trunc(record.measure_ts / 1000))
    fit.write_weight_scale(
        timestamp=math.trunc(record.measure_ts / 1000),
        weight=float(record.weight * 0.45359237),
        percent_fat=float(record.body_fat),
        percent_hydration=float(record.body_water),
        visceral_fat_mass=float(record.body_vfr),
        bone_mass=float(record.bone_mineral),
        muscle_mass=float(record.muscle),
        basal_met=float(record.bmr),
        physique_rating=float(record.body_type),
        active_met=int(float(record.bmr) * 1.25),
        metabolic_age=float(record.metabolic_age),
        visceral_fat_rating=float(record.body_vfr),
        bmi=float(record.bmi),
    )
    fit.finish()
    try:
        with open(fname, "ab") as fitfile:
            fitfile.write(fit.getvalue())
            print(f"Fit file {fname} updated")
    except OSError as e:
        print(f"Got an error writing {fname}: {e}")
  

try:
    client = Client(token=os.environ['WYZE_ACCESS_TOKEN'])
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)
    records = client.scales.get_records(start_time=start_time, end_time=end_time)
    print(f"Found {len(records)} scale records")
    for record in records:
        write_scale_data(record)
except WyzeApiError as e:
    # You will get a WyzeApiError if the request failed
    print(f"Got an error: {e}")
