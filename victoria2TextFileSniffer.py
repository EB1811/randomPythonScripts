from os import listdir
from os.path import isfile, join
import os
import random

myPath = 'D:/Users/Emmanuils/Documents/GamesStuff/Victoria.II.v3.04.Inclu.ALL.DLC/Victoria.II.v3.04.Inclu.ALL.DLC/mod/EMAN_MoreCivilised/history/provinces/indonesia'
corePath = 'D:/Users/Emmanuils/Documents/GamesStuff/Victoria.II.v3.04.Inclu.ALL.DLC/Victoria.II.v3.04.Inclu.ALL.DLC/mod/EMAN_MoreCivilised'
countryListPath = '/Users/Emmanuils/Documents/Victoria.II.v3.04.Inclu.ALL.DLC\Victoria.II.v3.04.Inclu.ALL.DLC/mod/GFM/history/countries'

# Get countries
#for subdir, dirs, files in os.walk(countryListPath):
 #   for file in files:
  #      filepath = subdir + os.sep + file
   #     dirname = subdir.split(os.path.sep)[-1]
#
 #       countryList.append(file[0] + file[1] + file[2])


# Create province files
def changeProvinces(country):
    for subdir, dirs, files in os.walk(myPath):
        for file in files:
            filepath = subdir + os.sep + file
            dirname = subdir.split(os.path.sep)[-1]
            newPath = 'D:/Users/Emmanuils/PythonFiles/'
            print('New Path', newPath)
            
            if not os.path.exists(newPath):
                os.makedirs(newPath)
                print("CREATING FILEPATH")

            if filepath.endswith(".txt"):
                readFrom = open(filepath, "r")
                writeToF = open(newPath+'/'+file, "w+")
                
                writeToF.write("owner = " + country + "\n")
                writeToF.write("controller = " + country + "\n")
                writeToF.write("add_core = " + country + "\n")
                for line in readFrom:
                    if "trade_goods" in line:
                        writeToF.write(line)
                    if "life_rating" in line:
                        writeToF.write(line)

                writeToF.close()
                readFrom.close()

                print(filepath)
                
def changeSpecificProvinces(initCountry, newCountry):
    for subdir, dirs, files in os.walk(myPath):
        for file in files:
            filepath = subdir + os.sep + file
            dirname = subdir.split(os.path.sep)[-1]
            newPath = 'D:/Users/Emmanuils/PythonFiles/'
            print('New Path', newPath)
            
            if not os.path.exists(newPath):
                os.makedirs(newPath)
                print("CREATING FILEPATH")

            if filepath.endswith(".txt"):
                readFrom = open(filepath, "r")

                isInitCountry = False

                for line in readFrom:
                    if "owner" in line:
                        if initCountry in line:
                            isInitCountry = True
                            
                readFrom.close()
                        
                if isInitCountry == True:
                    writeToF = open(newPath+'/'+file, "w+")
                    readFromInner = open(filepath, "r")
                
                    writeToF.write("owner = " + newCountry + "\n")
                    writeToF.write("controller = " + newCountry + "\n")
                    writeToF.write("add_core = " + newCountry + "\n")
                    for line in readFromInner:
                        if "trade_goods" in line:
                            writeToF.write(line)
                        if "life_rating" in line:
                            writeToF.write(line)

                    writeToF.close()
                    readFromInner.close()
                    
                    print(filepath)
                else:
                    readFrom.close()
                
def changeSpecificPops(path, newPath, countries, multiplier):
    for subdir, dirs, files in os.walk(path):
        for file in files:
            filepath = subdir + os.sep + file
            dirname = subdir.split(os.path.sep)[-1]

            if filepath.endswith(".txt"):
                for countryName in countries:
                    if countryName in filepath:
                        readFrom = open(filepath, "r")
                        writeToF = open(newPath+'/'+file, "w+")

                        for line in readFrom:
                            if "size" in line:
                                size = round(int(line.split('=')[-1]) * multiplier)
                                writeToF.write("		size = " + str(size) + "\n")
                            else:
                                writeToF.write(line)

                        readFrom.close()

                        print(countryName)

def getGivenCountries(path, newPath, countries):
    for subdir, dirs, files in os.walk(path):
        for file in files:
            filepath = subdir + os.sep + file
            dirname = subdir.split(os.path.sep)[-1]

            if filepath.endswith(".txt"):
                for tag in countries:
                    if tag in filepath:
                        readFrom = open(filepath, "r")
                        writeToF = open(newPath+'/'+file, "w+")

                        countryInfo = []
                        for line in readFrom:
                            writeToF.write(line)
                            countryInfo.append(line)

                        readFrom.close()

                        print(tag)
                        print(countryInfo)

# changeProvinces("INO")
changeSpecificProvinces("PHI", "PHL")
# changeSpecificPops(corePath + '/history/pops/1836.1.1', 'D:/Users/Emmanuils/PythonFiles/', ['Vietnam', 'Burma', 'Philippines', 'Malaysia', 'Indonesia', 'Cambodia'], 1.35)
# getGivenCountries(corePath + '/history/countries', 'D:/Users/Emmanuils/PythonFiles/', ['BUR', 'IND', 'INO', 'DAI', 'ANN', 'SIA', 'PAT'])
print("DONE")
