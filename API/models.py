import os

from django.db import models
import pandas as pd


class RawImageModel(models.Model):
    floor_plan = models.ImageField()


class FloorPlanCompartments:
    closet = 0
    bathroom = 0
    living_room = 0
    bedroom = 0
    hall = 0
    door = 0


class FloorPlansCsvData:

    def __init__(self):
        self.file_names = []
        self.closet_count = []
        self.bathroom_count = []
        self.living_room_count = []
        self.bedroom_count = []
        self.hall_count = []
        self.door_window_count = []

    def append_special(self, file_name, nr_closets, nr_bathrooms, nr_living_rooms, nr_bedrooms, nr_halls,
                       nr_doors_windows):
        self.file_names.append(file_name)
        self.closet_count.append(nr_closets)
        self.bathroom_count.append(nr_bathrooms)
        self.living_room_count.append(nr_living_rooms)
        self.bedroom_count.append(nr_bedrooms)
        self.hall_count.append(nr_halls)
        self.door_window_count.append(nr_doors_windows)

    def to_csv(self):
        csv_file_name = "tmp/data.csv"
        if os.path.exists(csv_file_name):
            os.remove(csv_file_name)
        data = {
            "file_name": self.file_names,
            "nr_closets": self.closet_count,
            "nr_bathrooms": self.bathroom_count,
            "nr_living_rooms": self.living_room_count,
            "nr_bedrooms": self.bedroom_count,
            "nr_halls": self.hall_count,
            "nr_doors_windows": self.door_window_count
        }
        df = pd.DataFrame(data)
        # compression_opts = dict(method='zip', archive_name='data.csv') compression=compression_opts
        return df.to_csv(csv_file_name, index=False)
