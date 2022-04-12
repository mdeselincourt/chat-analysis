import codecs, sys, re

pattern = '(.*?)\|(.*?)\|(.*)'
regex = re.compile(pattern)

corpus = []
lastPerson = ""

with codecs.open("../normalised.txt", encoding='utf-8') as file:
    
    i = 0
    wholeMessage = ""

    for line in file.readlines():
        
        i += 1

        matches = re.search(pattern,line)

        if matches is None:
            sys.exit()
        else:
            datetime = matches.group(1)
            person = matches.group(2)
            message = matches.group(3)

            #print("Person is " + person)

            if (person == lastPerson):
                # Same person as previous; just append text to the last entry
                corpus[-1] += ("¦ " + message.strip())
            else:
                # first of a batch, write headers and message
                wholeMessage = "|".join([datetime,person,message.strip()])
                corpus.append(wholeMessage)
                lastPerson = person

with open('../prepared.txt','w',encoding='utf-8-sig') as outputFile:
    for m in corpus:
        outputFile.write(m)  
        outputFile.write('\n')  
