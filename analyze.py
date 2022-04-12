import codecs, sys, re

pattern = '(.*?)\|(.*?)\|(.*)'

variables = {}

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

            subposts = message.count("¦")

            variables[person] = {"subposts": variables["person"]["subposts"] += subposts}

print(variables)