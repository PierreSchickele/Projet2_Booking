import pandas as pd
import numpy as np

hotel_infos = pd.read_json("projet_booking/spiders/bookingscrap.json")

hotel_infos['stars'] = hotel_infos['stars'].apply(lambda x: None if x==0 else x)

