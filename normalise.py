import codecs, sys, re

messagePattern = '(\d\d\/\d\d\/\d\d\d\d,\s\d\d:\d\d) - (.*?):(.*)'
infoPattern = '(\d\d\/\d\d\/\d\d\d\d,\s\d\d:\d\d) - (.*?)'

mentionRegex = re.compile('@(\d+)')
# urlRegex = re.compile('(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
urlRegex = re.compile('(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')

corpus = []
lastPerson = ""

with codecs.open("../um21.txt", encoding='utf-8') as file:
    i = 0
    wholeMessage = ""
    for line in file.readlines():
        
        i += 1 

        messageMatches = re.search(messagePattern,line)
        if messageMatches is None:

            infoMatches = re.search(infoPattern, line)
            if infoMatches is None:
                # > Looks like a newline in a message
                wholeMessage += line.strip() # Remove the spare line return and append it
            else:
                pass # > looks like a system message, do nothing (i.e. drop line)
        else:
            # > Looks like a new message start
            datetime = messageMatches.group(1)
            person = messageMatches.group(2)
            message = messageMatches.group(3)

            message = message.replace(":|","😐") # Neutral Face
            message = message.replace(";)","😉") # Winking Face
            message = message.replace(":)","☺️") # Smiling Face
            message = message.replace(":(","🙁") # :( = Slightly Frowning Face
            message = message.replace("^^","😊") # ^^ = Smiling Face with Smiling Eyes

            # Cleanse remaining unfound pipes
            message = message.replace("|","")
            message = message.replace("<Media omitted>","@MEDIA")

            message = mentionRegex.sub("@MENTION", message)

            message = urlRegex.sub("@URL", message)

            wholeMessage = "|".join([datetime,person,message])
            corpus.append(wholeMessage) # Dump the buffered message

        # OK

with open('../normalised.txt','w',encoding='utf-8-sig') as outputFile:
    for m in corpus:
        outputFile.write(m)  
        outputFile.write('\n')  
