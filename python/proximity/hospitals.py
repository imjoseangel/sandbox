#!/usr/bin/env python
# -*- coding: utf-8 -*-

import geopandas as gp
from pygris import tracts

# Coordinate system: State Plane South Dakota North
sd_tracts = tracts("SD", cb=True,
                   year=2021,
                   cache=True).to_crs(6571)

hospital_url = "https://opendata.arcgis.com/api/v3/datasets/6ac5e325468c4cb9b905f1728d6fbf0f_0/\
downloads/data?format=geojson&spatialRefId=4326"


hospitals = gp.read_file(hospital_url).to_crs(6571)

trauma = hospitals.loc[hospitals['TRAUMA'].str.contains(
    "LEVEL I\\b|LEVEL II\\b|RTH|RTC")]

trauma = trauma.drop_duplicates(['ID'])
