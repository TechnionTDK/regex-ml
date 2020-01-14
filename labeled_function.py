import re

# avoid tag
from snorkel.labeling import labeling_function

ABSTAIN = -1

# tag
REF = 1

# not tag
NO_REF = 0

# Global strings array containing "Masachtot" names
MASACHTOT_BAVLI = ['דברכות', 'ברכות', 'פאה', 'דמאי', 'כלאים', 'שביעית', 'תרומות', 'מעשרות', 'מעשר שני', 'חלה',
                   'ערלה', 'ביכורים', 'שבת', 'דשבת', 'עירובין', 'ערובין', 'פסחים', 'שקלים', 'יומא', 'סוכה', 'ביצה',
                   'ראש השנה', 'תענית', 'דתענית',
                   'מגילה', 'מועד קטן', 'חגיגה', 'יבמות', 'כתובות', 'נדרים', 'נזיר', 'סוטה', 'גיטין', 'גטין',
                   'קידושין', 'קדושין',
                   'בבא קמא', 'בבא מציעא', 'בבא בתרא', 'סנהדרין', 'מכות', 'שבועות', 'עבודה זרה', 'עדיות', 'עדויות',
                   'הוריות', 'אבות',
                   'זבחים', 'מנחות', 'חולין', 'בכורות', 'ערכין', 'תמורה', 'כריתות', 'מעילה', 'תמיד', 'מדות', 'קינים',
                   'כלים', 'אהלות', 'נגעים', 'פרה', 'טהרות', 'מקוואות', 'נדה', 'מכשירין', 'זבים', 'טבול יום', 'ידים',
                   'עוקצין']

'''we added spaces after some combinations '''
PRAKIM = ['ובפרק ', 'פרק', 'בפרק ', 'בפ\"ב', 'פ\"ק', 'בסוף פרק', 'פירקא', 'בפ\' ', 'ופ\' ', 'פ\' ', 'סוף פרק', 'דבפרק ',
          'דפרק', 'ב\"ק']


@labeling_function()
def if_parenthesis(x):
    """check if data contain ()"""
    pattern1 = '.*\(.*\)'
    result = re.match(pattern1, x.text)
    if result:
        return REF
    else:
        if ("(" in x.text and (")" not in x.text)) or (")" in x.text and ("(" not in x.text)):
            return NO_REF
        else:
            return ABSTAIN


@labeling_function()
def if_perek(x):
    """check if contains chapter or versions of it"""
    for perek in PRAKIM:
        if perek in x.text:
            return REF
    return ABSTAIN


'''
@labeling_function()
def if_begins_with_perek(x):
    """check if n-gram begins with perek or version of it"""
    for perek in PRAKIM:
        pattern = '^'+perek
        result = re.match(pattern, x.text)
        if result:
            return REF
    return ABSTAIN
'''


@labeling_function()
def if_begin_or_end_of_perek(x):
    """check if contains בבתרא או בקמא"""
    return REF if "קמא" in x.text or "בבתרא" in x.text else ABSTAIN


@labeling_function()
def if_amod(x):
    """check if contains amood"""
    # TODO: check whether to change parenthesis direction.
    return REF if ".)" in x.text or ":)" in x.text else ABSTAIN


@labeling_function()
def if_mashechet(x):
    """check if contains mashechet"""
    for mashechet in MASACHTOT_BAVLI:
        if mashechet in x.text:
            return REF
    return ABSTAIN


@labeling_function()
def if_daf(x):
    """check if contains page"""
    return REF if " דף" in x.text or "(דף" in x.text else ABSTAIN


# after evrything work add this func
@labeling_function()
def check_if_berish_and_perek(x):
    """check if in the same sentence there is a brish+perek"""
    for perek in PRAKIM:
        if perek in x.text and 'בריש' in x.text:
            return REF
    return ABSTAIN


garbage_words = ["משנה","כלים","שבת"]
@labeling_function()
def check_mishna(x):
    """mark NO_REF if contains 'mishna'"""
    for word in garbage_words:
        if word in x.text:
            return NO_REF
    return ABSTAIN
    #return NO_REF if "משנה" in x.text or "כלים" in or "" in x.text else ABSTAIN


@labeling_function()
def check_legal_paren_num(x):
    flag = False  # check if n gram contains any parenthesis in the first place
    counter = 0
    for letter in x.text:

        if letter == ')':
            flag = True
            counter += 1
            continue
        if letter == '(':
            flag = True
            counter -= 1
        if counter < 0:
            return NO_REF
    if counter == 0 and flag:
        return REF
    if counter > 0:
        return NO_REF
    if counter == 0 and flag is False:
        return ABSTAIN
