import sys
import os
import ijson





def ReadChats():
    if(len(sys.argv)) <= 1:
        print("No file Path Provided")
        return None
    filename = sys.argv[1]#"result.json"
    print(filename)
    if not os.path.exists(filename):
        print("File does not exist")
        return None

    names = {}
    with open(filename, "rb") as f:
        for record in ijson.items(f, "messages"):
            for message in record:
                # print(message['text'])
                if message['type'] == "message":
                    #names
                    if not isinstance(message['text'], str):
                        length = 1
                    else:
                        length = len(message['text'].split())
                    if message['from'] in names.keys():
                        names[message['from']]['count']  += 1
                        names[message['from']]['length']  += length
                        
                        #months
                        if message['date'][0:7] in names[message['from']]['month'].keys():
                            names[message['from']]['month'][message['date'][0:7]] += 1
                        else:
                            names[message['from']]['month'][message['date'][0:7]] = 1
                        #date
                        if message['date'][0:10] in names[message['from']]['date'].keys():
                            names[message['from']]['date'][message['date'][0:10]] += 1
                        else:
                            names[message['from']]['date'][message['date'][0:10]] = 1

                        #time
                        if message['date'][11:13] in names[message['from']]['time'].keys():
                            names[message['from']]['time'][message['date'][11:13]] += 1
                        else:
                            names[message['from']]['time'][message['date'][11:13]] = 1

                        #words
                        if isinstance(message['text'], str):
                            for i in message['text'].split():
                                if len(i) < 4:
                                    continue
                                if i.lower() in names[message['from']]['words'].keys():
                                    names[message['from']]['words'][i.lower()] += 1
                                else:
                                    names[message['from']]['words'][i.lower()] = 1



                    else:
                        month = message['date'][0:7]
                        date = message['date'][0:10]
                        time = message['date'][11:13]
                        names[message['from']] = {"count":1, "length": length,"month": { month : 1},"date": { date : 1},"time": { time : 1}, "words": {}}
                        if isinstance(message['text'], str):
                            for i in message['text'].split():
                                if len(i) < 4:
                                    continue
                                if i.lower() in names[message['from']]['words'].keys():
                                    names[message['from']]['words'][i.lower()] += 1
                                else:
                                    names[message['from']]['words'][i.lower()] = 1                        
    #print("Total : " + str(x))
    # print(names)
    # print(type(names))
    return names