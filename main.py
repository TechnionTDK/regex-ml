from snorkel.labeling import labeling_function
import pandas as pd
from nltk import ngrams
import re

from sklearn.model_selection import train_test_split
from snorkel.labeling import LabelModel
from snorkel.labeling import MajorityLabelVoter
from numpy import savetxt

# from utils import load_torat_emet_dataset

from snorkel.labeling import PandasLFApplier

from snorkel.labeling import LFAnalysis

from snorkel.analysis import get_label_buckets

# import snorkel.labeling
#@labeling_function()
#def idfdf(x):
#    pass

#avoid tag
ABSTAIN = -1

#tag
REF = 1

#not tag
NO_REF = 0
"maybe we have a rejection function"

SAMPLE_SIZE = 100
K_GRAM = 6


def split_into_sentences(text):
    if ".)" in text: text=text.replace(".)","<prd>)")
    sentences = text.split(".")
    text = text.replace("<prd>", ".")
    for s in sentences:
        s = s.replace("<prd>", ".")
        print(s)
    return sentences


def load_torat_emet_data(): #TODO:in example it is in utils, in our case it is here, so transfer func
    df = pd.read_csv('csvRes.csv')
    data = ''
    k_gram_series = pd.Series()
    for x in range(SAMPLE_SIZE):
        data = df['text'][x]
        for sentence in split_into_sentences(data):
            k_gram_series_for_one = pd.Series(generate_ngrams(sentence, K_GRAM))
            k_gram_series= k_gram_series.append(k_gram_series_for_one, ignore_index=True)
    #print(k_gram_series)
   # k_gram_series = pd.Series(generate_ngrams(whole_text, K_GRAM))

    data_frame = pd.DataFrame({'text': k_gram_series})
    #print(data_frame.size)
    data_frame['tag'] = ABSTAIN
    training_set, test_set = train_test_split(data_frame, test_size=0.2)
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
    return REF if ")." in x.text or "):" in x.text else ABSTAIN



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



def create_devset(train_set):
    dev = pd.DataFrame(columns=('text', 'tag'))
    counter = 0
    print("the size is : ", train_set.size)
    for index, row in train_set.iterrows():
        print(row['text'])
        ans = input("please tag : 1 is tag and 0 is untag")
        new_row = {'text': row['text'], 'tag': ans}
        dev = dev.append(new_row, ignore_index=True)
        if ans is '1':
            counter = counter + 1
        if counter == 50:
            break
    dev.to_csv(r'C:\private\Shaked\Technion\shaked_technion\winter 2019-2020\project_new\dev.csv', index=False)
    return dev


def run_lf_on_data():
    df_train, df_test = load_torat_emet_data()
    df_dev = pd.read_csv('dev_22.12.csv')
    df_train.to_csv(r'C:\private\Shaked\Technion\shaked_technion\winter 2019-2020\project_new\df_train.csv',
                    index=False)

    #df_dev = create_devset(df_train)
    print(f"Dev REF frequency: {100 * (df_dev.tag.values == REF).mean():.1f}%")

    #TODO: when creating test and dev, use split function
    #TODO: -to devide 50/50 between them
    Y_dev = df_dev.tag.values
    #TODO:add validation set and dev set

    lfs = [if_parenthesis, if_perek, if_daf, if_mashechet,
           if_amod, if_begin_or_end_of_perek]

    applier = PandasLFApplier(lfs=lfs)
    l_train = applier.apply(df=df_train)

    l_dev = applier.apply(df=df_dev)

    coverage_if_parenthesis, coverage_if_perek, coverage_if_daf, coverage_if_mashechet,\
    coverage_if_amod, coverage_if_begin_or_end_of_perek = (l_train != ABSTAIN).mean(axis=0)

    print(f"coverage_if_parenthesis: {coverage_if_parenthesis * 100:.1f}%")
    print(f"coverage_if_perek: {coverage_if_perek * 100:.1f}%")
    print(f"coverage_if_daf: {coverage_if_daf * 100:.1f}%")
    print(f"coverage_if_mashechet: {coverage_if_mashechet * 100:.1f}%")
    print(f"coverage_if_amod: {coverage_if_amod * 100:.1f}%")
    print(f"coverage_if_begin_or_end_of_perek: {coverage_if_begin_or_end_of_perek * 100:.1f}%")


    #label_model = LabelModel(cardinality=2, verbose=True)
    #label_model.fit(L_train=l_train, n_epochs=500, lr=0.001, log_freq=100, seed=123)

    print("=======")
    print(" summary of l_train ")
    print(LFAnalysis(L=l_train, lfs=lfs).lf_summary())
    print(" summary of l_dev - only tagged ")
    print(LFAnalysis(L=l_dev, lfs=lfs).lf_summary(Y=Y_dev))


# part c - see what lf mislabeled and compare with other lfs
    buckets = get_label_buckets(Y_dev, l_dev[:, 1])
    print(" indexes of ngram where lf mislabeled ")
    print(df_dev.iloc[buckets[(NO_REF, REF)]])

    print(" check what this lf caught - check if_mashecet - will be 10 samples")
    print(df_train.iloc[l_train[:, 3] ==REF].sample(10, random_state=1))


    majority_model = MajorityLabelVoter()
    preds_train = majority_model.predict(L=l_train)

    #TODO: compare this model with other model
    print(" === result ===")
    print (preds_train)
    #for debuging, exe preds train to file
    #savetxt('preds_t',preds_train, delimiter=',')

    #put predicted labels in df train
    df_train['tag'] = preds_train

    print("final")
    print(df_train)
    df_train.to_csv(r'C:\private\Shaked\Technion\shaked_technion\winter 2019-2020\project_new\labeled_data.csv', index=False)


def main():
    load_torat_emet_data()
    # run_lf_on_data()
    #df_train, df_test = load_torat_emet_data()
    #dev = create_devset(df_train)


if __name__ == "__main__":
    main()

