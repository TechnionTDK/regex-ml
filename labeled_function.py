import re

#avoid tag
from snorkel.labeling import labeling_function

ABSTAIN = -1

#tag
REF = 1

#not tag
NO_REF = 0


# Global strings array containing "Masachtot" names
MASACHTOT_BAVLI = ['דברכות','ברכות', 'פאה', 'דמאי', 'כלאים', 'שביעית', 'תרומות', 'מעשרות', 'מעשר שני', 'חלה',
                   'ערלה', 'ביכורים', 'שבת','דשבת', 'עירובין', 'ערובין', 'פסחים', 'שקלים', 'יומא', 'סוכה', 'ביצה',
                   'ראש השנה', 'תענית','דתענית',
                   'מגילה', 'מועד קטן', 'חגיגה', 'יבמות', 'כתובות', 'נדרים', 'נזיר', 'סוטה', 'גיטין', 'גטין',
                   'קידושין', 'קדושין',
                   'בבא קמא', 'בבא מציעא', 'בבא בתרא', 'סנהדרין', 'מכות', 'שבועות', 'עבודה זרה', 'עדיות', 'עדויות',
                   'הוריות', 'אבות',
                   'זבחים', 'מנחות', 'חולין', 'בכורות', 'ערכין', 'תמורה', 'כריתות', 'מעילה', 'תמיד', 'מדות', 'קינים',
                   'כלים', 'אהלות', 'נגעים', 'פרה', 'טהרות', 'מקוואות', 'נדה', 'מכשירין', 'זבים', 'טבול יום', 'ידים',
                   'עוקצין']


@labeling_function()
def if_parenthesis(x):
    """check if data contain ()"""
    pattern = '.*\(.*\).*'
    result = re.match(pattern, x.text)
    if result:
        return REF
    else:
        return ABSTAIN

@labeling_function()
def if_perek(x):
    """check if contains chapter or versions of it"""
    return REF if "פרק" in x.text or "בפרק" in x.text or "בפ'" in x.text or "בפ\"ב" in x.text\
                  or "בפ\"ק" in x.text or "בסוף פרק" in x.text or "פירקא" in x.text else ABSTAIN


@labeling_function()
def if_begin_or_end_of_perek(x):
    """check if contains בבתרא או בקמא"""
    return REF if "בקמא" in x.text or "בבתרא" in x.text else ABSTAIN
#TODO add also קמא בתרא mabye we need change the check , here it maby substring and catch בקמאות


@labeling_function()
def if_amod(x):
    """check if contains amood"""
    #TODO: check whether to change parenthesis direction.
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
    return REF if "דף" in x.text else ABSTAIN
