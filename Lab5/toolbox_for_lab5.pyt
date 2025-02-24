# -*- coding: utf-8 -*-
import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "GarageBuildingIntersections"
        self.alias = "GarageBuildingIntersections"

        # List of tool classes associated with this toolbox
        self.tools = [GarageBuildingIntersections]


class GarageBuildingIntersections(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Lab 5 toolbox"
        self.description = "Find garages on the TAMU campus closest to a specific building"
        self.canRunInBackground = False #will only be allowed to run in ArcMap
        self.category = "Building Tools"

    def getParameterInfo(self):
        #Define the tool parameters.
        #Parameter0 asks for the name of the GDB Folder
        param0 = arcpy.Parameter(
            displayName = "GDB Folder",
            name = "GDBFolder",
            datatype = "DEFolder", #specify location for data to be stored
            parameterType = "Required",
            direction = "Input"
            )
        #Prameter1 asks for the name of the geodatabase
        param1 = arcpy.Parameter(
            displayName = "GDB Name",
            name = "GDBName",
            datatype = "GPString", #input will be a text value
            parameterType = "Required",
            direction = "Input"
            )
        #Parameter2 specifies the csv file
        param2 = arcpy.Parameter(
            displayName = "Garage CSV File",
            name = "GarageCSVFile",
            datatype = "DEFile", #save as a file on the disk
            parameterType = "Required",
            direction = "Input"
            )
        #Parameter3 asks for the name of the layer
        param3 = arcpy.Parameter(
            displayName = "Garage Layer Name",
            name = "Garage Layer Name",
            datatype = "GPString", #input will be a text value
            parameterType = "Required",
            direction = "Input"
            )
        #Parameter4 will ask for the gdb that already exists for the purpose of our tool
        param4 = arcpy.Parameter(
            displayName = "Campus GDB",
            name = "CampusGDB",
            datatype = "DEWorkspace", #specify an existing gdb
            parameterType = "Required",
            direction = "Input"
            )
        #Parameter5 asks for the buffer distance
        param5 = arcpy.Parameter(
            displayName = "Buffer Distance",
            name = "BufferDistance",
            datatype = "GPDouble", #a double position number
            parameterType = "Required",
            direction = "Input"
            )

        params = [param0, param1, param2, param3, param4, param5]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameter, messages):
        """The source code of the tool."""
        folder_path = parameter[0].valueAsText
        gdb_name = parameter[1].valueAsText
        gdb_path = folder_path + '\\' + gdb_name
        arcpy.CreateFileGDB_management(folder_path, gdb_name)

        #import the csv file to arcgis pro
        csv_path = parameter[2].valueAsText
        glayer_name = parameter[3].valueAsText
        garage = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', glayer_name) #the path, the column names, the new created layer's name; garage is the layer

        #saving the feature layer to our geodatabase
        input_layer = garage
        arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path) #the layer we need going into the path we have
        garage_points = gdb_path + '\\' + glayer_name #adds the new feature layer to our existing geodatabase path

        #open the campus geodatabase, copy building features into OUR geodatabase
        campus = parameter[4].valueAsText
        campus_buildings = campus + '\\Structures'
        buildings = gdb_path + '\\' + 'Buildings' #adds the bulding features to the geodatabase

        arcpy.Copy_management(campus_buildings, buildings) #structures is in campus builing gdb, we need to copy that feature and it will be called buildings

        #Re-projection
        #desc= arcpy.Describe(buildings)
        spatial_ref = arcpy.Describe(buildings).spatialReference #extracts the spatial reference from the buildings layer
        arcpy.management.Project(garage_points, gdb_path + '\Garage_Points_reprojected', spatial_ref) #the layer we're reprojecting, the name of the result

        #buffer the garages
        buffer_distance = int(parameter[5].value)
        garage_buffer = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_reprojected',gdb_path + '\Garage_Points_buffered')

        #Make the buffer intersect with buildings
        arcpy.Intersect_analysis([garage_buffer, buildings], gdb_path + '\Garage_Building_Intersection', 'ALL')
        #[the two layers], the result

        #Put the results in a table
        arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersection.dbf', r'C:\Users\leahmrdz22\MataRodriguez-online-GEOG676-spring2025\Lab5', 'ClosestBuildings.csv')

        return None