from os import listdir
from os.path import isfile, join
import os
import random
import re

def stmExpenseFormatterHSBC(stm):
    lastPriceIndex = 0
    for i, char in enumerate(stm[::-1].strip()):
        if char and not(char.isdigit() or char == '.'):
            lastPriceIndex = len(stm) - (i + 1)
            break

    date = stm[0:9]
    info = re.sub(r'[()*#]', '', stm[20:lastPriceIndex])
    price = stm[lastPriceIndex:]

    return (date.strip(), info.strip(), price.strip())

def statementTextSniffer(path, resultPath):
    for subdir, dirs, files in os.walk(path):
        for file in files:
            filepath = subdir + os.sep + file
            dirname = subdir.split(os.path.sep)[-1]
            
            print('New Path', resultPath)
            if not os.path.exists(resultPath):
                os.makedirs(resultPath)
                print("CREATING FILEPATH")

            if filepath.endswith(".txt"):
                readFrom = open(filepath, "r")
                writeToF = open(resultPath+"/restult.txt", "a+")
                
                print(filepath)
                writeToF.write(filepath + "\n\n")

                groups = {}
                
                for line in readFrom:
                    if "PAYMENT" not in line:
                        (date, info, price) = stmExpenseFormatterHSBC(line)
                        print(date, info, price)
                        groups[info] = round(groups.get(info, 0) + float(price))

                print("\nResults:\n")
                total = 0
                for group, price in groups.items():
                    total += price
                    print(group + ': ' + str(price))
                    writeToF.write(group + ': ' + str(price) + "\n")
                    
                print("---Total---")
                print(total)
                writeToF.write("---Total---\n")
                writeToF.write(str(total) + "\n\n")
    
                writeToF.close()
                readFrom.close()

# stmExpenseFormatterHSBC("")
statementTextSniffer("C:/Users/Eman/Desktop/money/raw", "C:/Users/Eman/Desktop/money")
