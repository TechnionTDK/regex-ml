import re
from utility import SHMOT_PRAKIM
from utility import MASACHTOT_BAVLI
from utility import ABSTAIN
from utility import REF
from utility import NO_REF
from snorkel.labeling import labeling_function


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
def mashechet_and_sham(x):
    """check if data contain mashechet and שם """
    count = 0
    """check if contains mashechet"""
    for mashechet in MASACHTOT_BAVLI:
        if mashechet in x.text:
            count = 1
    """finish with שם """
    pattern1 = '.*(שם)$'
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
    """finish with שם """
    pattern1 = '.*(שם)$'
    result = re.match(pattern1, x.text)
    if result:
        count += 1

    if count >= 2:
        return REF
    return ABSTAIN


@labeling_function()
def daf_in_parntes(x):
    """check if data contain daf in parents and finish with parenthesis """
    """finish with parenthesis"""
    pattern1 = '.*(([(].*דף.*[)])[:]?)$'
    result = re.match(pattern1, x.text)
    if result:
        return REF
    return ABSTAIN


@labeling_function()
def no_double_parans(x):
    """ Check if data contains more then one left/right parenthesis """
    if x.text.count("(") > 1 or x.text.count(")") > 1:
        return NO_REF
    if x.text.count("(") != x.text.count("("):
        return NO_REF
    return ABSTAIN

@labeling_function()
def no_mishna(x):
    """ Check if data contains the world mishna """
    if 'משנה' in x.text:
        return NO_REF
    return ABSTAIN
