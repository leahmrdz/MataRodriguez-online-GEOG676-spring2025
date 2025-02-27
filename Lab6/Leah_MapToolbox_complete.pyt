# -*- coding: utf-8 -*-

import arcpy
import time


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]


class GraduatedColorsRenderer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "graduatedcolor" #display name in arcgis pro
        self.description = "create a graduated color map based on a specific attribute layer"
        self.canRunInBackground = False
        self.category = "MapTools"

    def getParameterInfo(self):
        """Define the tool parameters."""
        #Parameter0 asks for the project name
        param0 = arcpy.Parameter(
            displayName = "ArcGIS Pro Project Name", #the name of the input seen in ArcGIS Pro
            name = "aprxInputName",
            datatype = "DEFile", #a file on a disk; a project package file
            parameterType = "Required",
            direction = "Input"
        )

        #Parameter1 asks for the layer that will be used in the color map
        param1 = arcpy.Parameter(
            displayName = "Layer to Classify", #the name of the input seen in ArcGIS Pro
            name = "LayertoClassify",
            datatype = "GPLayer", #a reference to a data source such as a shapefile, gdb, feature class, etc. 
            parameterType = "Required",
            direction = "Input"
        )

        #Parameter2 asks where the output will be saved
        param2 = arcpy.Parameter(
            displayName = "Output Location", #the name of the input seen in ArcGIS Pro
            name = "OutputLocation",
            datatype = "DEFolder", #specifies location where data will be stored 
            parameterType = "Required",
            direction = "Input"
        )

        #Parameter3 asks what the output project name will be
        param3 = arcpy.Parameter(
            displayName = "Output Project Name", #the name of the input seen in ArcGIS Pro
            name = "OutputProjectName",
            datatype = "GPString", #input will be in string form
            parameterType = "Required",
            direction = "Input"
        )

        params = [param0, param1, param2, param3]
        return params
######
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
######
    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Make and define the progessor tool
        readTime = 3 #the time the progessor titles will be visible for the user
        start = 0 #the starting position for the progressor
        max = 100 #progressor's end position
        step = 33 #progress intervals for the progressor

        #initial progressor values
        arcpy.SetProgressor ("step", "Valodating Project File...", start, max, step) #type of progressor, message, min, max, step
        time.sleep(readTime) #pause time for 3 seconds so the user can read the message defined above
        #The message shown in the results pane
        arcpy.AddMessage("Validating Project File...")

        #access the input project file
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)
        #grab the first instance of a map from the .aprx
        campus = project.listMaps('Map')[0] #campus will be the first map in the project file

        #when the above block of code runs, the progressor can begin its incrementation
        arcpy.SetProgressorPosition(start + step) #now 33% complete
        arcpy.SetProgressorLabel("Finding your map layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")

        #Loop through the layers of the first map/campus
        for layer in campus.listLayers():
            #check if the layer is a feature layer
            if layer.isFeatureLayer:
                #copy the layer's symbology
                symbology = layer.symbology
                #make sure the symbology has renderer attribute
                if hasattr(symbology,'renderer'):
                    #Check layer name
                    if layer.name == parameters[1].valueAsText: #checking the layer name matches the input layer

                        #progressor increments again
                        arcpy.SetProgressorPosition(start + step) #now 33% complete
                        arcpy.SetProgressorLabel("Calculating and classifying...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating and classifying...")

                        #update the copy's renderer to 'graduated colors renderer'
                        symbology.updateRenderer('GraduatedColorsRenderer')

                        #tell arcpy which field will be used to create the colored map
                        symbology.renderer.classificationField = "Shape_Area" #using the polygons' shape area

                        #progressor increments again
                        arcpy.SetProgressorPosition(start + step*2) #now 66% complete
                        arcpy.SetProgressorLabel("Cleaning up...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Cleaning up and...")

                        #how many classes the map will have
                        symbology.renderer.breakCount = 5
                        #set color ramp
                        symbology.renderer.colorRamp = project.listColorRamps('Blues (5 Classes)')[0]

                        #set the layer's symbology equal to the copy's
                        layer.symbology = symbology

                        arcpy.AddMessage("Finish Generating Layer...")
                    else:
                        print("No Feature Layers found")

        #progressor increments again
        arcpy.SetProgressorPosition(start + step*3) #now 99% complete
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")

        project.saveACopy(parameters[2].valueAsText + "\\" + parameters[3].valueAsText + ".aprx")
        #copy will be in folder location under the new project name

        return

