from os import listdir
from os.path import isfile, join
import os
import json
from matplotlib import pyplot

corePath = 'D:/Users/Emmanuils/Documents/GamesStuff/vic2_economy_analyzer-0.12/Hisotry'

def extractCountriesInfo(countryTags, wantedInfo, divisionInfo = None, path = corePath + '/swiss.history'):
    with open(path, "r") as file:
        data = json.load(file)

        #{date: countries[]}
        processedDates = []

        dates = data['history']
        for date, dateGameData in dates.items():
            if date.endswith('.1.1'):
                formattedCountries = []
                
                requestedCountries = list(filter(lambda c: c['tag'] in countryTags, dateGameData['countries']))
                
                if len(requestedCountries) != len(countryTags):
                    for missingTag in filter(lambda t: t not in map(lambda c: c['tag'], dateGameData['countries']), countryTags):
                        formattedCountries.append({"tag": missingTag, "data": 0})
                
                for country in requestedCountries:
                    wantedCalcData = country[wantedInfo] / country[divisionInfo] if divisionInfo else country[wantedInfo]
                    formattedCountries.append({"tag": country['tag'], "data": wantedCalcData})
                
                processedDates.append({"date": date, "countries": formattedCountries})

        #print(sorted(processedDates, key = lambda pd: pd['date']))
        return sorted(processedDates, key = lambda pd: pd['date'])

def createHistoryGraph(countryTags, wantedInfo, divisionInfo = None):
    processedDates = extractCountriesInfo(countryTags, wantedInfo, divisionInfo)
    
    dates = list(map(lambda pd: pd['date'], processedDates))
    dateCountries = list(map(lambda pd: pd['countries'], processedDates))

    countryData = []
    for tag in countryTags:
        countryData.append({"tag": tag,
            "dataPoints": list(map(lambda cs:  next(c for c in cs if c['tag'] == tag)['data'], dateCountries))
        })
    #print(countryData)

        
    for data in countryData:
        pyplot.plot(dates, data['dataPoints'], label = data['tag'])
        #, marker='o'

    pyplot.legend()
    pyplot.show()

#processedDates = extractCountriesInfo(['FRA', 'USA', 'ENG', 'NEJ'], 'gdp')
createHistoryGraph(['FRA', 'USA', 'TUR', 'ENG', 'HND', 'RUS', 'AUS', 'PRU', 'NGF', 'KUK', 'SWI'], 'gdp')
createHistoryGraph(['INO', 'BEL', 'CHL', 'HAI', 'SER', 'SWI'], 'gdp')
#, 'population'
