from os import listdir
from os.path import isfile, join
import os
import random

myPath = 'D:/Users/Emmanuils/Documents/GamesStuff/Victoria.II.v3.04.Inclu.ALL.DLC/Victoria.II.v3.04.Inclu.ALL.DLC/mod/EMAN_MoreCivilised/history/provinces/india'
corePath = 'D:/Users/Emmanuils/Documents/GamesStuff/Victoria.II.v3.04.Inclu.ALL.DLC/Victoria.II.v3.04.Inclu.ALL.DLC/mod/EMAN_MoreCivilised'
countryListPath = '/Users/Emmanuils/Documents/Victoria.II.v3.04.Inclu.ALL.DLC\Victoria.II.v3.04.Inclu.ALL.DLC/mod/TGC/history/countries'

# Get countries
#for subdir, dirs, files in os.walk(countryListPath):
 #   for file in files:
  #      filepath = subdir + os.sep + file
   #     dirname = subdir.split(os.path.sep)[-1]
#
 #       countryList.append(file[0] + file[1] + file[2])


# Create province files
def changeProvinces(country, path = corePath + '/history/provinces/india', newPath = 'D:/Users/Emmanuils/PythonFiles/'):
    for subdir, dirs, files in os.walk(path):
        for file in files:
            filepath = subdir + os.sep + file
            dirname = subdir.split(os.path.sep)[-1]
            
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
                
def changeSpecificProvinces(initCountry, newCountry, path = corePath + '/history/provinces/asia', newPath = 'D:/Users/Emmanuils/PythonFiles/'):
    for subdir, dirs, files in os.walk(path):
        for file in files:
            filepath = subdir + os.sep + file
            dirname = subdir.split(os.path.sep)[-1]
            
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

def getRandomPopCountryNamesList(countriesPath, amount):
    countryNames = []
    for subdir, dirs, files in os.walk(countriesPath):
        randomFiles = random.sample(files, amount)
        for file in randomFiles:
            countryNames.append(file.split('.', 1)[0])
    print(countryNames)
    return countryNames

                        
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

### CORE ###
# changeProvinces("INO")
# changeSpecificProvinces("EIC", "BUR")
# changeSpecificPops(corePath + '/history/pops/1836.1.1', 'D:/Users/Emmanuils/PythonFiles/', ['Vietnam', 'Burma', 'Philippines', 'Malaysia', 'Indonesia', 'Cambodia'], 1.35)
# changeSpecificPops(corePath + '/history/pops/1836.1.1', 'D:/Users/Emmanuils/PythonFiles/', ['China', 'India'], 0.75)
# getGivenCountries(corePath + '/history/countries', 'D:/Users/Emmanuils/PythonFiles/', ['BUR', 'IND', 'INO', 'DAI', 'ANN', 'SIA', 'PAT'])

### EXTRA ###
#changeSpecificPops(corePath + '/history/pops/1836.1.1', 'D:/Users/Emmanuils/PythonFiles/', getRandomPopCountryNamesList(corePath + '/history/pops/1836.1.1', 10), 0.5)
changeSpecificPops(corePath + '/history/pops/1836.1.1', 'D:/Users/Emmanuils/PythonFiles/', getRandomPopCountryNamesList(corePath + '/history/pops/1836.1.1', 10), 2)

print("DONE")

#getRandomPopCountryNamesList(corePath + '/history/pops/1836.1.1', 5)
