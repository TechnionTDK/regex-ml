import numpy as np
from utility import SHMOT_PRAKIM
from utility import MASACHTOT_BAVLI
from snorkel.augmentation import transformation_function


def choose_random(itm,lst):
    if len(lst) < 2: return itm
    while True:
        chosen = np.random.choice(lst)
        if chosen is not itm:
            return chosen

@transformation_function()
def change_perek(x):
    for perek in SHMOT_PRAKIM:
        # perek_ident = " " + perek + " "
        if perek in x.text:
            new_perek = choose_random(perek,SHMOT_PRAKIM)
            x.text = x.text.replace(perek,new_perek)
            return x
    return None

@transformation_function()
def change_masechet(x):
    for masechet in MASACHTOT_BAVLI:
        # masechet_ident = " "+masechet+" "
        if masechet in x.text:
            new_masechet = choose_random(masechet,MASACHTOT_BAVLI)
            x.text = x.text.replace(masechet,new_masechet)
            return x
    return None
