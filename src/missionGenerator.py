import pymap3d
import math

class MissionGenerator:
    def __init__(self):
        pass

    def setPOI(self, lat, lon, altEGM96):
        """Set position of Point of Interest.

        Args:
            lat (float): POI latitude WGS84
            lon (float): POI longitude WGS84
            altEGM96 (float): POI absolute altitude EGM96
        """        
        self.POI_lat = lat
        self.POI_lon = lon
        self.POI_altEGM96 = altEGM96
        self.POI_altRel = 0

    def setWaitDuration(self, duration):
        """Set duration of wait action.

        Args:
            duration (int): duration in seconds
        """        
        self.waitDuration = duration

    def getPOI(self):
        """Point of Interest getter.

        Returns:
            dict: dictionnary containing POI, field are "lat", "lon", "altAbs"
        """        
        return {"lat": self.POI_lat, "lon": self.POI_lon, "altRel": self.POI_altRel}

    def range2focalLength(slef, range):
        # some mapping between the two, maybe include the size of observed object
        return 200

    def generateTransect(self, setHeading, setAltRel, setDist):
        """Generate waypoints for a set of transects mission.
        The mission is a set of waypoints placed on the cylindrical grid described by setHeading, setAltRel and setDist.
        At each waypoint, a picture is taken, looking at the POI.

        Args:
            setHeading (list): list of headings in degrees
            setAltRel (list): list of altitudes relative to POI in meters
            setDist (list): list of distances from the POI in meters

        Returns:
            list: waypoint list, can be passed to the wpmlTemplate to generate a DJI mission file
        """        
        wp = []
        sind = lambda degrees: math.sin(math.radians(degrees))
        cosd = lambda degrees: math.cos(math.radians(degrees))
        
        # For all wapoints
        for heading in setHeading:
            for alt in setAltRel:
                for dist in setDist:
                    # Compute absolute position from relative offsets
                    lat, lon, altRel = pymap3d.enu2geodetic(dist * sind(heading), dist * cosd(heading), alt, self.POI_lat, self.POI_lon, self.POI_altRel)

                    # Compute set of gimbal positions
                    az, el, srange = pymap3d.geodetic2aer(self.POI_lat, self.POI_lon, self.POI_altRel, lat, lon, altRel)
                    # Create waypoint
                    wp.append(
                        {"lat": lat, "lon": lon, "altRel": altRel, "actions": [
                            # {"pitch": el, "yaw": az, "focalLength": self.range2focalLength(srange)}
                            {"type": "Wait", "duration": self.waitDuration},
                            {"type": "TakePhoto"},
                    ]}
                    )
        return wp
    
if __name__ == "__main__":
    gen = MissionGenerator()
    gen.setPOI(51.42354723804961, -2.670840695536882, 48)
    wp = gen.generateTransect([90], [70, 100, 120], [100, 150, 200, 250])
    print(wp)