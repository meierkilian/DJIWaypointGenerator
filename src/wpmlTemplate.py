import uuid
import time
import os
from zipfile import ZipFile

class WpmlTemplate:
    def __init__(self):
        pass

    def getActionOrientedShoot(self, pitch, yaw, focalLength, wpID, imgID):
        # TODO: check if aircraftHeading and gimbalYawRotateAngle really have to be the same?
        actionUUID = uuid.uuid4()
        action = f"""<wpml:action>
                <wpml:actionId>{imgID}</wpml:actionId>
                <wpml:actionActuatorFunc>orientedShoot</wpml:actionActuatorFunc>
                <wpml:actionActuatorFuncParam>
                    <wpml:gimbalPitchRotateAngle>{pitch}</wpml:gimbalPitchRotateAngle>
                    <wpml:gimbalRollRotateAngle>0</wpml:gimbalRollRotateAngle>
                    <wpml:gimbalYawRotateAngle>{yaw}</wpml:gimbalYawRotateAngle>
                    <wpml:focusX>0</wpml:focusX>
                    <wpml:focusY>0</wpml:focusY>
                    <wpml:focusRegionWidth>0</wpml:focusRegionWidth>
                    <wpml:focusRegionHeight>0</wpml:focusRegionHeight>
                    <wpml:focalLength>{focalLength}</wpml:focalLength>
                    <wpml:aircraftHeading>{yaw}</wpml:aircraftHeading>
                    <wpml:accurateFrameValid>0</wpml:accurateFrameValid>
                    <wpml:payloadPositionIndex>0</wpml:payloadPositionIndex>
                    <wpml:useGlobalPayloadLensIndex>0</wpml:useGlobalPayloadLensIndex>
                    <wpml:targetAngle>0</wpml:targetAngle>
                    <wpml:actionUUID>{actionUUID}</wpml:actionUUID>
                    <wpml:imageWidth>0</wpml:imageWidth>
                    <wpml:imageHeight>0</wpml:imageHeight>
                    <wpml:AFPos>0</wpml:AFPos>
                    <wpml:gimbalPort>0</wpml:gimbalPort>
                    <wpml:orientedCameraType>66</wpml:orientedCameraType>
                    <wpml:orientedFilePath>{actionUUID}</wpml:orientedFilePath>
                    <wpml:orientedFileMD5/>
                    <wpml:orientedFileSize>0</wpml:orientedFileSize>
                    <wpml:orientedFileSuffix>{f'img_WP{wpID}_{imgID}'}</wpml:orientedFileSuffix>
                    <wpml:orientedPhotoMode>normalPhoto</wpml:orientedPhotoMode>
                </wpml:actionActuatorFuncParam>
            </wpml:action>
            """
        return action
        
    def getPlaceMarks(self, wp, wpID):
        actions = ""
        for actionID, a in enumerate(wp["actions"]):
            actions += self.getActionOrientedShoot(a["pitch"], a["yaw"], a["focalLength"], wpID, actionID)
        
        # <wpml:ellipsoidHeight>{0}</wpml:ellipsoidHeight>
        placeMarks = f"""<Placemark>
        <Point>
            <coordinates>
                {wp['lon']},{wp['lat']}
            </coordinates>
        </Point>
        <wpml:index>{wpID}</wpml:index>
        <wpml:height>{wp['altAbs']}</wpml:height>
        <wpml:useGlobalHeight>0</wpml:useGlobalHeight>
        <wpml:useGlobalSpeed>1</wpml:useGlobalSpeed>
        <wpml:useGlobalHeadingParam>1</wpml:useGlobalHeadingParam>
        <wpml:useGlobalTurnParam>1</wpml:useGlobalTurnParam>
        <wpml:gimbalPitchAngle>0</wpml:gimbalPitchAngle>
        <wpml:useStraightLine>0</wpml:useStraightLine>
        <wpml:actionGroup>
            <wpml:actionGroupId>{wpID}</wpml:actionGroupId>
            <wpml:actionGroupStartIndex>{wpID}</wpml:actionGroupStartIndex>
            <wpml:actionGroupEndIndex>{wpID}</wpml:actionGroupEndIndex>
            <wpml:actionGroupMode>sequence</wpml:actionGroupMode>
            <wpml:actionTrigger>
                <wpml:actionTriggerType>reachPoint</wpml:actionTriggerType>
            </wpml:actionTrigger>
            {actions}
        </wpml:actionGroup>
        <wpml:isRisky>0</wpml:isRisky>
    </Placemark>
    """
        return placeMarks


    def getWaypointMission(self, wpList, POI, takeOffSecurityHeight = 20, globalTransitionalSpeed = 5, autoFlightSpeed = 5, globalHeightOffset = 50):
        # Generated PlaceMark list, i.e. waypoints
        placeMarks = ""
        for id, wp in enumerate(wpList):
            placeMarks += self.getPlaceMarks(wp, id)
        creationTime = round(time.time()*1e3) # Unix epoch in milisecs
        mission = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:wpml="http://www.dji.com/wpmz/1.0.6">
<Document>
    <wpml:createTime>{creationTime}</wpml:createTime>
    <wpml:updateTime>{creationTime}</wpml:updateTime>
    <wpml:missionConfig>
        <wpml:flyToWaylineMode>safely</wpml:flyToWaylineMode>
        <wpml:finishAction>goHome</wpml:finishAction>
        <wpml:exitOnRCLost>executeLostAction</wpml:exitOnRCLost>
        <wpml:executeRCLostAction>goBack</wpml:executeRCLostAction>
        <wpml:takeOffSecurityHeight>{takeOffSecurityHeight}</wpml:takeOffSecurityHeight>
        <wpml:globalTransitionalSpeed>{globalTransitionalSpeed}</wpml:globalTransitionalSpeed>
        <wpml:droneInfo>
            <wpml:droneEnumValue>77</wpml:droneEnumValue>
            <wpml:droneSubEnumValue>0</wpml:droneSubEnumValue>
        </wpml:droneInfo>
        <wpml:payloadInfo>
            <wpml:payloadEnumValue>66</wpml:payloadEnumValue>
            <wpml:payloadSubEnumValue>0</wpml:payloadSubEnumValue>
            <wpml:payloadPositionIndex>0</wpml:payloadPositionIndex>
        </wpml:payloadInfo>
    </wpml:missionConfig>
    <Folder>
    <wpml:templateType>waypoint</wpml:templateType>
    <wpml:templateId>0</wpml:templateId>
    <wpml:waylineCoordinateSysParam>
        <wpml:coordinateMode>WGS84</wpml:coordinateMode>
        <wpml:heightMode>EGM96</wpml:heightMode>
        <wpml:positioningType>GPS</wpml:positioningType>
    </wpml:waylineCoordinateSysParam>
    <wpml:autoFlightSpeed>{autoFlightSpeed}</wpml:autoFlightSpeed>
    <wpml:globalHeight>{POI["altAbs"] + globalHeightOffset}</wpml:globalHeight>
    <wpml:caliFlightEnable>0</wpml:caliFlightEnable>
    <wpml:gimbalPitchMode>usePointSetting</wpml:gimbalPitchMode>
    <wpml:globalWaypointHeadingParam>
        <wpml:waypointHeadingMode>towardPOI</wpml:waypointHeadingMode>
        <wpml:waypointHeadingAngle>0</wpml:waypointHeadingAngle>
        <wpml:waypointPoiPoint>{POI["lat"]},{POI["lon"]},{POI["altAbs"]}</wpml:waypointPoiPoint>
        <wpml:waypointHeadingPoiIndex>0</wpml:waypointHeadingPoiIndex>
    </wpml:globalWaypointHeadingParam>
    <wpml:globalWaypointTurnMode>toPointAndStopWithDiscontinuityCurvature</wpml:globalWaypointTurnMode>
    <wpml:globalUseStraightLine>1</wpml:globalUseStraightLine>
    {placeMarks}
    <wpml:payloadParam>
        <wpml:payloadPositionIndex>0</wpml:payloadPositionIndex>
        <wpml:meteringMode>average</wpml:meteringMode>
        <wpml:dewarpingEnable>0</wpml:dewarpingEnable>
        <wpml:returnMode>singleReturnStrongest</wpml:returnMode>
        <wpml:samplingRate>240000</wpml:samplingRate>
        <wpml:scanningMode>nonRepetitive</wpml:scanningMode>
        <wpml:modelColoringEnable>0</wpml:modelColoringEnable>
    </wpml:payloadParam>
    </Folder>
</Document>
</kml>"""

        return mission
    
    def generateMissionArchive(self, fileName, mission):
        with ZipFile(f"{fileName}.kmz", "w") as myzip:
            myzip.writestr(os.path.join("wpmz","template.kml"), mission)
                

if __name__ == '__main__':
    templates = WpmlTemplate()
    wp = [ 
        {"lat": 51.4233553605864, "lon": -2.671656658289393, "altAbs": 100, "actions": [
            {"pitch": 4, "yaw": 5, "focalLength": 6},
            {"pitch": 7, "yaw": 8, "focalLength": 9},
        ]},
        {"lat": 51.4235404797627, "lon": -2.6708493698988263, "altAbs": 100, "actions": [
            {"pitch": 4, "yaw": 5, "focalLength": 6},
            {"pitch": 7, "yaw": 8, "focalLength": 9},
        ]},
    ]
    str = templates.getWaypointMission(wp, {"lat": 51.42307121304408, "lon": -2.6710493996958298, "altAbs": 47})
    templates.generateMissionArchive("newCoolMission1", str)
    
    