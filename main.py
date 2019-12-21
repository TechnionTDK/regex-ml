from snorkel.labeling import labeling_function
import pandas as pd
from nltk import ngrams
import re

from sklearn.model_selection import train_test_split
from snorkel.labeling import LabelModel
from snorkel.labeling import MajorityLabelVoter


# from utils import load_torat_emet_dataset

from snorkel.labeling import PandasLFApplier


# import snorkel.labeling
#@labeling_function()
#def idfdf(x):
#    pass

#avoid tag
ABSTAIN = -1

#tag
REF = 1

#not tag
UNTAG = 0
"maybe we have a rejection function"

SAMPLE_SIZE = 2
K_GRAM = 6
def load_torat_emet_data(): #TODO:in example it is in utils, in our case it is here, so transfer func
    whole_text = csv_to_string()
    #TODO: avoid creating sample that is half end of line k and half beginning of line k+1
    k_gram_series = pd.Series(generate_ngrams(whole_text, K_GRAM))
    data_frame = pd.DataFrame({'text':k_gram_series})
    data_frame['tag'] = ABSTAIN
    training_set, test_set = train_test_split(data_frame, test_size=0.2)
    #print(training_set)
    return training_set, test_set
    #print(data_frame) #now we have untagged df





def csv_to_string():
    df = pd.read_csv('csvRes.csv')
    data =''
    print(df.shape[0])
    #TODO: or real run change 50 to df.shape[0]
    for x in range(SAMPLE_SIZE):
        data+= df['text'][x]
    #print(data)
    return data


def generate_ngrams(s, n):
    # Convert to lowercases
    s = s.lower()

    # Replace all none alphanumeric characters with spaces
    # s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)

    # Break sentence in the token, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]
  
    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]










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
    return REF if "(" in x.text and ")" in x.text else ABSTAIN
#TODO change to regular expresion

@labeling_function()
def if_perek(x):
    """now we see if contain פרק or varsion of it"""
    return REF if "פרק" in x.text or "בפרק" in x.text or "בפ'" in x.text or "בפ\"ב" in x.text\
                  or "בפ\"ק" in x.text or "בסוף פרק" in x.text or "פירקא" in x.text else ABSTAIN


@labeling_function()
def if_begin_or_end_of_perek(x):
    """now we see if contain בבתרא או בקמא"""
    return REF if "בקמא" in x.text or "בבתרא" in x.text else ABSTAIN
#TODO add also קמא בתרא mabye we need change the check , here it maby substring and catch בקמאות


@labeling_function()
def if_amod(x):
    """now we see if contain (. or (:  יכול להיות שנצטרך לשנות את הסוגר לצד השני כתלות בטקסט"""
    return REF if ")." in x.text or "):" in x.text else ABSTAIN



@labeling_function()
def if_mashechet(x):
    """now we see if contain mashechet"""
    for mashechet in MASACHTOT_BAVLI:
        if mashechet in x.text:
            return REF
    return ABSTAIN


@labeling_function()
def if_daf(x):
    """now we see if contain daf"""
    return REF if "דף" in x.text else ABSTAIN





def run_lf_on_data():
    df_train, df_test = load_torat_emet_data()
    Y_test = df_test.tag.values
    #TODO:add validation set and dev set
    lfs = [if_parenthesis, if_perek, if_daf, if_mashechet, if_amod, if_begin_or_end_of_perek]

    applier = PandasLFApplier(lfs=lfs)
    l_train = applier.apply(df=df_train)
    # print(l_train)
   # L_dev = applier.apply(df=df_dev)

    coveragefl = []
    coveragefl = (l_train != ABSTAIN).mean(axis=0)
    counter=0
    '''
    for x in coveragefl:
        print(f" {x}: {coveragefl[counter] * 100:.1f}%")
        counter += 1
  
    label_model = LabelModel(cardinality=2, verbose=True)
    label_model.fit(L_train=l_train, n_epochs=500, lr=0.001, log_freq=100, seed=123)
    '''

    majority_model = MajorityLabelVoter()
    preds_train = majority_model.predict(L=l_train)
    print(preds_train)

    for x in range(preds_train.size):
        df_train['tag'][x]=preds_train[x]

    print(df_train)

#אנו רוצים שהדאטאפריים שלנו יכיל 2 עמודות text label
#Y_dev = df_dev.label.values
#Y_valid = df_valid.label.values






def main():
    #csv_to_string()
    # s = "a b c d e sdf next next1 next2 next3"
    # new = generate_ngrams(s, 6)
    #print((new))
    run_lf_on_data()


if __name__ == "__main__":
    main()







#this is how we print it
#print(f"check_out coverage: {coverage_check_out * 100:.1f}%")
#print(f"check coverage: {coverage_check * 100:.1f}%")

