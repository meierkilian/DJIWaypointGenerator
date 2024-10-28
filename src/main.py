from missionGenerator import MissionGenerator
from wpmlTemplate import WpmlTemplate

gen = MissionGenerator()
templates = WpmlTemplate()

gen.setPOI(51.42354723804961, -2.670840695536882, 48)
wp = gen.generateTransect(90, [70, 100, 120], [100, 150, 200, 250])
str = templates.getWaypointMission(wp, gen.getPOI())
templates.generateMissionArchive("newCoolMission", str)

