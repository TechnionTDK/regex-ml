import codecs

# Global strings array containing "Masachtot" names
MASACHTOT_BAVLI = ['ברכות', 'פאה', 'דמאי', 'כלאים', 'שביעית', 'תרומות', 'מעשרות', 'מעשר שני', 'חלה',
                   'ערלה', 'ביכורים', 'שבת', 'עירובין', 'ערובין', 'פסחים', 'שקלים', 'יומא', 'סוכה', 'ביצה',
                   'ראש השנה', 'תענית',
                   'מגילה', 'מועד קטן', 'חגיגה', 'יבמות', 'כתובות', 'נדרים', 'נזיר', 'סוטה', 'גיטין', 'גטין',
                   'קידושין', 'קדושין',
                   'בבא קמא', 'בבא מציעא', 'בבא בתרא', 'סנהדרין', 'מכות', 'שבועות', 'עבודה זרה', 'עדיות', 'עדויות',
                   'הוריות', 'אבות',
                   'זבחים', 'מנחות', 'חולין', 'בכורות', 'ערכין', 'תמורה', 'כריתות', 'מעילה', 'תמיד', 'מדות', 'קינים',
                   'כלים', 'אהלות', 'נגעים', 'פרה', 'טהרות', 'מקוואות', 'נדה', 'מכשירין', 'זבים', 'טבול יום', 'ידים',
                   'עוקצין']


def isMasechet(word):
    if(word in MASACHTOT_BAVLI):
        return True
    return False


def addMatch(matches, start, end):
    matches.append((start,end))


def doMatches(matches,text):

    for current_index in range(0, len(text)):
        if (text[current_index] == '('):
            start = current_index + 1
            i = current_index + 1
            word = ""
            while (text[i] != " " and text[i] != ")"):
                word += text[i]
                i += 1
            if isMasechet(word):
                while (text[i] != ")"):
                    i += 1
                end = i - 1
                addMatch(matches, start, end)
            current_index = i
    """ 
    print(matches)
    print(len(matches))
    for match in matches:
        s, e = match
        while (s != e + 1):
            print(text[s], end='')
            s += 1
        print("")
    """


def makeJSON(matches,text):

    match_string = """{"examples":[{"string":" """
    match_string += text.replace('\n',' ').replace('\"',' ')

    match_string += """ " , "match":[ """
    for match in matches:
        s,e = match
        match_string +="{"
        match_string += """ "start":{0},"end":{1}""".format(s,e)
        match_string +="},"
    match_string = match_string[:-1]  # remove last char
    match_string+="]}]}"

    return match_string


def main():
    text = ""
    with open("tora.txt", encoding='utf-8') as f:
        text = f.read()
    matches = []

    print("-Parsing text and find matches...")
    doMatches(matches, text)

    print("-Converting into JSON format...")
    json_string = makeJSON(matches, text)

    print("-Creating JSON file...")
    with open("data_file.json", 'w', encoding='utf8') as json_file:
        json_file.write(json_string)

    print("JSON File created! contains: [{0}] matches.".format(len(matches)))


if __name__ == "__main__":
    main()

