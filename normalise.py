import codecs, sys, re

messagePattern = '(\d\d\/\d\d\/\d\d\d\d,\s\d\d:\d\d) - (.*):(.*)'
infoPattern = '(\d\d\/\d\d\/\d\d\d\d,\s\d\d:\d\d) - (.*)'

corpus = []

with codecs.open("../um21.txt", encoding='utf-8') as file:
    i = 0
    wholeMessage = ""
    for line in file.readlines():
        
        i += 1 

        messageMatches = re.search(messagePattern,line)
        if messageMatches is None:

            infoMatches = re.search(infoPattern, line)
            if infoMatches is None:
                # Looks like a newline in a message
                wholeMessage += line.strip() # make it not a newline
            else:
                pass # looks like an info line, do nothing
        else:
            # Looks like a new message start
            datetime = messageMatches.group(1)
            person = messageMatches.group(2)
            message = messageMatches.group(3)

            wholeMessage = ",".join([datetime,person,message])
            corpus.append(wholeMessage) # Dump the buffered message

        # OK

with open('../normalised.txt','w',encoding='utf-8-sig') as outputFile:
    for m in corpus:
        outputFile.write(m)  
