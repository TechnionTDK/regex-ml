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

SHMOT_PRAKIM = ['הקורא עומד', 'בני העיר', 'הקורא למפרע']


@labeling_function()
def masechet_then_parans(x):
    """check if data contain mashechet and finish with parenthesis """
    count = 0
    """check if contains mashechet"""
    for mashechet in MASACHTOT_BAVLI:
        if mashechet in x.text:
            count = 1
    """finish with parenthesis"""
    pattern1 = '.*([(].*[)])$'
    result = re.match(pattern1, x.text)
    if result:
        count += 1
    if count >= 2:
        return REF
    return ABSTAIN


@labeling_function()
def perek_then_parans(x):
    """check if data contain perek and finish with parenthesis """
    count = 0
    """check if contains perek"""
    for perek in SHMOT_PRAKIM:
        if perek in x.text:
            count = 1
    """finish with parenthesis"""
    pattern1 = '.*([(].*[)])$'
    result = re.match(pattern1, x.text)
    if result:
        count += 1
    if count >= 2:
        return REF
    return ABSTAIN


@labeling_function()
def perek_and_sham(x):
    """check if data contain perek and שם """
    count = 0
    """check if contains perek"""
    for perek in SHMOT_PRAKIM:
        if perek in x.text:
            count = 1
    """finish with parenthesis"""
    if "שם" in x.text:
        count += 1
    if count >= 2:
        return REF
    return ABSTAIN


@labeling_function()
def mashechet_and_sham(x):
    """check if data contain mashechet and שם """
    count = 0
    """check if contains mashechet"""
    for mashechet in MASACHTOT_BAVLI:
        if mashechet in x.text:
            count = 1
    if "שם" in x.text:
        count += 1
    if count >= 2:
        return REF
    return ABSTAIN


@labeling_function()
def daf_in_parntes(x):
    """check if data contain daf in parents and finish with parenthesis """
    """finish with parenthesis"""
    pattern1 = '.*([(].*דף.*[)])$'
    result = re.match(pattern1, x.text)
    if result:
        return REF
    return ABSTAIN


@labeling_function()
def no_double_parans(x):
    """ Check if data contains more then one left/right parenthesis """
    if x.count('(') > 1 or x.count(')') > 1:
        return NO_REF
    else:
        return ABSTAIN

