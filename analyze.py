import sys
import codecs # for unicode
import re # for regular expressions
import pprint # for logging

pattern = '(.*?)\|(.*?)\|(.*)'

obscenities = [[],[],[],[],[]]
obscenities[4] = ["fuck"]
obscenities[3] = ["bastard","cock","dick","knob","prick","twat"]
obscenities[2] = ["balls", "bitch", "bollock", "shit","piss"]
obscenities[1] = ["arse","bloody","bugger","crap","damn"]

v = {}

log = []

with codecs.open("../prepared.txt", encoding='utf-8') as file:
    i = 0
    wholeMessage = ""
    for line in file.readlines():
        i += 1 
        matches = re.search(pattern,line)
        if matches is None:
            sys.exit(1)
        else:
            datetime = matches.group(1)
            person = matches.group(2)
            message = matches.group(3)

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
                    "emojiDict": {},
                    "swearDict": {}
                }
            else:
                # Person exists and needs to have their basic stats update
                v[person]["utterances"] += 1
                v[person]["lines"] += lines
                v[person]["words"] += words
                v[person]["media"] += media
                v[person]["mentions"] += mentions
                v[person]["urls"] += urls

            emoji = {}
            emojis = 0
            # Update person's emoji stats

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
            for rank in obscenities:
                for cuss in rank:
                    n = message.count(cuss)
                    if n > 0:
                        if cuss not in v[person]["swearDict"]:
                            v[person]["swearDict"][cuss] = n
                        else:
                            v[person]["swearDict"][cuss] += n

columns = []

for p in v:
    for key in v[p]:
        if key not in columns:
            columns.append(key)
    columns.remove("emojiDict")
    columns.remove("swearDict")
    for e in v[p]["emojiDict"]:
        if e not in columns:
            columns.append(e)
    for s in v[p]["swearDict"]:
        if s not in columns:
            columns.append(s)
        
columns = sorted(columns)
columns.insert(0,"NAME")
matrix = []
matrix.append(columns)

# iterate through columns
for p in v:
    newPersonRow = [p]
    for col in columns[1:]: # Skip first column as it's "NAME"
        log.append("searching for " + col)
        if col in v[p]:
            # column is a first order child of the person
            newPersonRow.append(v[p][col]) 
            
        else:
            if col in v[p]["emojiDict"]:
                newPersonRow.append(v[p]["emojiDict"][col])
            
            else:
                if col in v[p]["swearDict"]:
                    newPersonRow.append(v[p]["swearDict"][col])
                    
                else:
                    newPersonRow.append(0)
    matrix.append(newPersonRow)
    log.append("Row for " + p + " is " + str(newPersonRow))

with open('../log.txt','w',encoding='utf-8-sig') as outputFile:
    for m in log:
        outputFile.write(m)  
        outputFile.write('\n')  

with open('../analysis.txt','w',encoding='utf-8-sig') as outputFile:
    for row in matrix:
        outputFile.write(str(row))
        outputFile.write('\n')



