from missionGenerator import MissionGenerator
from wpmlTemplate import WpmlTemplate

gen = MissionGenerator()
templates = WpmlTemplate()

gen.setPOI(0.027602345792634667, 36.90306379850778, 0)
gen.setWaitDuration(30)
wp = gen.generateTransect(setHeading=[0], setAltRel=[70, 100, 120], setDist=[200, 300, 400])
str = templates.getWaypointMission(wp, gen.getPOI())
templates.generateMissionArchive("output/localisation_test", str)

