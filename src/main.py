from missionGenerator import MissionGenerator
from wpmlTemplate import WpmlTemplate

gen = MissionGenerator()
templates = WpmlTemplate()

gen.setPOI(0.06493547056984221, 36.8712012772987, 0)
gen.setWaitDuration(13)
wp = gen.generateTransect(setHeading=[150], setAltRel=[50, 85, 120], setDist=[100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600])

str = templates.getWaypointMission(wp, gen.getPOI())
templates.generateMissionArchive("output/localisation_WaterHoleNorth_20250202_1", str)

