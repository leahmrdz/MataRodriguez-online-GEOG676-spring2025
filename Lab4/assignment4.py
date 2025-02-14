import arcpy

#set workspace and create geodatabase
arcpy.env.workspace = r'C:\Users\leahmrdz22\MataRodriguez-online-GEOG676-spring2025\Lab4\codes'
folder_path = r'C:\Users\leahmrdz22\MataRodriguez-online-GEOG676-spring2025\Lab4'
gdb_name = 'lab4base.gdb'
gdb_path = folder_path + '\\' + gdb_name
arcpy.CreateFileGDB_management(folder_path, gdb_name) #where the geodatabase is saved, and its name

#import the csv file to arcgis pro
csv_path = r'C:\Users\leahmrdz22\MataRodriguez-online-GEOG676-spring2025\Lab4\garages.csv'
glayer_name = 'Garage_Points'
garage = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', glayer_name) #the path, the column names, the new created layer's name; garage is the layer

#saving the feature layer to our geodatabase
input_layer = garage
arcpy.conversion.FeatureClassToGeodatabase(input_layer, r'C:\Users\leahmrdz22\MataRodriguez-online-GEOG676-spring2025\Lab4\lab4base.gdb') #the layer we need going into the path we have
garage_points = gdb_path + '\\' + glayer_name #adds the new feature layer to our existing geodatabase path

#open the campus geodatabase, copy building features into OUR geodatabase
campus = r'C:\Users\leahmrdz22\MataRodriguez-online-GEOG676-spring2025\Lab4\Campus.gdb'
campus_buildings = campus + '\Structures'
buildings = gdb_path + '\\' + 'Buildings' #adds the bulding features to the geodatabase

arcpy.Copy_management(campus_buildings, buildings) #structures is in campus builing gdb, we need to copy that feature and it will be called buildings

#Re-projection
spatial_ref = arcpy.Describe(buildings).spatialReference #extracts the spatial reference from the buildings layer
arcpy.management.Project(garage_points, gdb_path + '\Garage_Points_reprojected', spatial_ref) #the layer we're reprojecting, the name of the result

#buffer the garages
uinput = input("What is the buffer distance requested in meters?")
garage_buffer = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_reprojected',gdb_path + '\Garage_Points_buffered', int(uinput)) 
#the reprojected layer, the new result, the buffer distance in meters


#Make the buffer intersect with buildings
arcpy.Intersect_analysis([garage_buffer, buildings], gdb_path + '\Garage_Building_Intersection', 'ALL')
#[the two layers], the result

#Put the results in a table
arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersection.dbf', r'C:\Users\leahmrdz22\MataRodriguez-online-GEOG676-spring2025\Lab4150', 'BuildingsNearby.csv')

