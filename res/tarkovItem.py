# This class represents a single tarkov item
class tarkovItem:
    name = ""
    hideout_level = 0
    hideout_station = ""
    img_link = ""
    
    def __init__(self, name, hideout_level, hideout_station, img_link):
        self.name = name
        self.hideout_level = hideout_level
        self.hideout_station = hideout_station
        self.img_link = img_link
    