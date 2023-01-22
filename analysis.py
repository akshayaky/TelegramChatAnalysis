import ijson
import os.path
import json
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np
import sys

import chatReader
import plot

def PrintDetails(names):
    people = ""
    count = "Count : "
    length = "Length : "
    average = "Average : "
    personMonths = set()        
    personTimes = set()        
    for i in names.keys():
        people += i + " "
        count += str(names[i]['count']) + "  "
        length += str(names[i]['length']) + "  "
        average += str(names[i]['length']/names[i]['count']) + "  "
        personMonths.update((names[i]['month'].keys()))
        personTimes.update(names[i]['time'].keys())
        # for j in names[i]['month'].keys():
        #     print(a + " : "  + str(names[i]['month'][a]) + " : "  + str(names[j]['month'][a]))
        #     months.append()


    print(people)
    print(count)
    print(length)
    print(average)

    monthCount = ""
    personMonths = sorted(personMonths)
    personTimes = sorted(personTimes)
    
    # print(personMonths)
    for i in personMonths:

        for j in names.keys():
            if i not in names[j]['month'].keys():
                monthCount += "0 "
            else:
                monthCount += str(names[j]['month'][i]) + " "
        monthCount += "\n"
    # print(monthCount)

def main():
    names = {}
    filename = "stats.json"
    if os.path.exists(filename) and len(sys.argv) <= 1:
        f = open(filename, encoding='utf-8')
        names= json.load(f)
        # print(names)
        # names = json.loads(data) 
    else:
        print("Reading the result.json file")
        names = chatReader.ReadChats()
        if names is not None:
            if os.path.exists(filename):
                os.remove(filename)
            filehandler = open("stats.json", "x", encoding='utf-8')
            names_ = str(names)
            names_ = names_.replace("'", "\"")
            json.dump(names, filehandler, ensure_ascii=False)
            # filehandler.write(names_)
            # print(names)
        else:
            return None

    #PrintDetails(names)
    plot.PlotandSave(names)
    os.system("start AnalysisResult.html")
    

if __name__=="__main__":
    main()

