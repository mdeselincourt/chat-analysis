import sys
import codecs # for unicode
import re # for regular expressions
import pprint # for logging

obscenity = {
    "fuck": 4,
    "bastard": 3,
    "cock": 3,
    "dick": 3,
    "knob": 3,
    "prick": 3,
    "twat": 3,
    "balls": 2,
    "bitch": 2,
    "bollock": 2,
    "shit": 2,
    "piss": 2,
    "arse": 1,
    "bloody": 1,
    "bugger": 1,
    "crap": 1,
    "damn": 1
}

timeOffsets={
    "Clara Straimer": 3,
    "Alex Wade": 1,
    "Dee Segal": -5,
    "Gideon Jones": -8 
}

#pattern = '(.*?)\|(.*?)\|(.*)'

pattern = '(\d\d\/\d\d\/\d\d\d\d),\s(\d\d):\d\d\|(.*?)\|(.*)'

v = {}

log = []

with codecs.open("../prepared.txt", encoding='utf-8') as file:
    i = 0
    wholeMessage = ""
    for line in file.readlines():
        i += 1 
        matches = re.search(pattern,line)
        if matches is None:
            print("No matches!")
            sys.exit(1)
        else:
            date = matches.group(1)
            hour = matches.group(2)
            person = matches.group(3)
            message = matches.group(4)

            # Line and word analysis
            lines = message.count("¦") + 1
            words = len(message.split())
            media = message.count("@MEDIA")
            mentions = message.count("@MENTION")
            urls = message.count("@URL")

            # Update variables
            if person not in v:
                # Initialise a person with the details of this first line
                v[person] = { 
                    "utterances" : 1,
                    "lines" : lines,
                    "words" : words,
                    "media" : media,
                    "mentions" : mentions,
                    "urls" : urls,
                    "scovilles": 0,
                    "emojiDict": {},
                    "swearDict": {},
                    "hourDict": {}
                }
            else:
                # Person exists and needs to have their basic stats update
                v[person]["utterances"] += 1
                v[person]["lines"] += lines
                v[person]["words"] += words
                v[person]["media"] += media
                v[person]["mentions"] += mentions
                v[person]["urls"] += urls

            #log.append(str(v[person]))

            # Update time buckets
            if person in timeOffsets:
                lt = (int(hour) + timeOffsets[person]) % 24
                localTime = "h" + "{:02d}".format(lt)
            else:
                localTime = "h" + hour
            if (localTime) not in v[person]["hourDict"]:
                #log.append("This message from " + person + " at " + hour + " should be attributed to " + localTime)
                v[person]["hourDict"][localTime] = 1
            else:
                #log.append("Incrementing hour " + hour + " for " + person)
                v[person]["hourDict"][localTime] += 1

            # Update person's emoji stats
            emoji = {}
            emojis = 0
            for i in range(127744, 129782): # for each emoji
                if (message.count(chr(i)) > 0): # if there are any 
                    # log.append(line + " contains " + chr(i))
                    emojis += 1
                    if chr(i) not in v[person]["emojiDict"]: # Initialise this emoji for this person
                        v[person]["emojiDict"][chr(i)] = message.count(chr(i))
                    else:                       # increase total
                        v[person]["emojiDict"][chr(i)] += message.count(chr(i))

            if "emojicount" not in v[person]:
                v[person]["emojicount"] = emojis
            else:
                v[person]["emojicount"] += emojis


            # Obscenity analysis
            for cuss in obscenity:
                n = message.count(cuss)
                if n > 0:
                    if cuss not in v[person]["swearDict"]:
                        v[person]["swearDict"][cuss] = n
                    else:
                        v[person]["swearDict"][cuss] += n
                    v[person]["scovilles"] += (obscenity[cuss] * n)
                    #log.append(message)
                    #log.append(str(n) + " " + cuss + " brings " + person + " to " + str(v[person]["scovilles"]) + " Scovilles")

# Enumerate columns

columns = []

for p in v:
    for key in v[p]:
        if key not in columns:
            if key not in ["emojiDict", "swearDict", "hourDict"]:
                columns.append(key)
    for e in v[p]["emojiDict"]:
        if e not in columns:
            columns.append(e)
    for s in v[p]["swearDict"]:
        if s not in columns:
            columns.append(s)
    for h in v[p]["hourDict"]:
        if h not in columns:
            columns.append(h)
        
columns = sorted(columns)
columns.insert(0,"NAME")
matrix = []
matrix.append(columns)

# iterate through columns and build up each row
for p in v:
    personWords = v[p]["words"]
    #log.append(p + " wrote " + str(personWords))
    newPersonRow = [p]
    for col in columns[1:]: # Skip first column as it's "NAME"
        if col in v[p]:
            # column is a first order child of the person
            newPersonRow.append(v[p][col]) 
            #log.append("writing column " + col + " into row " + p)
        else:
            if col in v[p]["emojiDict"]:
                newPersonRow.append(v[p]["emojiDict"][col])
            
            else:
                if col in v[p]["swearDict"]:
                    newPersonRow.append(v[p]["swearDict"][col])
                    
                else:
                    if col in v[p]["hourDict"]:
                        newPersonRow.append(v[p]["hourDict"][col])
                    else:
                        newPersonRow.append(0)

    matrix.append(newPersonRow)

for colNum, colHeader in enumerate(columns):
    if colNum == 0: 
        continue
    log.append("scanning column " + str(colNum) + ", c = " + str(colHeader))
    colMax = 0
    # search for max
    for rowNum, row in enumerate(matrix):
        if rowNum == 0:
            continue
        colMax = max(colMax, int(row[colNum]))
        log.append("max " + colHeader + " is now " + str(colMax))
    # normalise
        
## END : OUTPUT LOGS AND RESULTS

with open('../log.txt','w',encoding='utf-8-sig') as outputFile:
    for m in log:
        outputFile.write(str(m))
        outputFile.write('\n')  

with open('../analysis.csv','w',encoding='utf-8-sig') as outputFile:
    for row in matrix:
        
        # This could probably be better
        output = str(row)

        output = output.replace("'","")
        output = output.replace("[","")
        output = output.replace("]","")

        outputFile.write(output)
        outputFile.write('\n')