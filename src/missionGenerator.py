import pymap3d
import math

class MissionGenerator:
    def __init__(self):
        pass

    def setPOI(self, lat, lon, altEGM96):
        self.POI_lat = lat
        self.POI_lon = lon
        self.POI_altEGM96 = altEGM96

    def getPOI(self):
        return {"lat": self.POI_lat, "lon": self.POI_lon, "altAbs": self.POI_altEGM96}

    def range2focalLength(slef, range):
        # some mapping between the two, maybe include the size of observed object
        return 30

    def generateTransect(self, heading, setAltRel, setDist):
        wp = []
        sind = lambda degrees: math.sin(math.radians(degrees))
        cosd = lambda degrees: math.cos(math.radians(degrees))
        
        # For all wapoints
        for alt in setAltRel:
            for dist in setDist:
                # Compute absolute position from relative offsets
                lat, lon, altAbs = pymap3d.enu2geodetic(dist * sind(heading), dist * cosd(heading), alt, self.POI_lat, self.POI_lon, self.POI_altEGM96)

                # Compute set of gimbal positions
                az, el, srange = pymap3d.geodetic2aer(self.POI_lat, self.POI_lon, self.POI_altEGM96, lat, lon, altAbs)
                # Create waypoint
                wp.append(
                    {"lat": lat, "lon": lon, "altAbs": altAbs, "actions": [
                        {"pitch": el, "yaw": az, "focalLength": self.range2focalLength(srange)}
                ]}
                )
        return wp
    
if __name__ == "__main__":
    gen = MissionGenerator()
    gen.setPOI(51.42354723804961, -2.670840695536882, 48)
    wp = gen.generateTransect(90, [70, 100, 120], [100, 150, 200, 250])
    print(wp)