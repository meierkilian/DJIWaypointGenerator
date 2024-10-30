from missionGenerator import MissionGenerator
from wpmlTemplate import WpmlTemplate

gen = MissionGenerator()
templates = WpmlTemplate()

gen.setPOI(51.42354723804961, -2.670840695536882, 48)
wp = gen.generateTransect([90, 110], [30, 40], [10, 20, 30])
str = templates.getWaypointMission(wp, gen.getPOI())
templates.generateMissionArchive("fenswoodWpTest_short", str)

