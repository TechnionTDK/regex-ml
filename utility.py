
from snorkel.labeling import labeling_function
import pandas as pd

from sklearn.model_selection import train_test_split


ABSTAIN = -1

# tag
REF = 1

# not tag

NO_REF = 0

SAMPLE_SIZE = 100
K_GRAM = 6
MIN_N_GRAM_SIZE = 3
MAX_N_GRAM_SIZE = 7


def split_into_sentences(text):
    if ".)" in text: text = text.replace(".)", "<prd>)")
    sentences = text.split(".")
    text = text.replace("<prd>", ".")
    for s in sentences:
        s = s.replace("<prd>", ".")
    return sentences


def load_torat_emet_data():  # TODO:in example it is in utils, in our case it is here, so transfer func
    df = pd.read_csv('csvRes.csv')
    data = ''
    k_gram_series = pd.Series()
    for x in range(SAMPLE_SIZE):
        data = df['text'][x]
        for sentence in split_into_sentences(data):
            for n_gram_size in range(MIN_N_GRAM_SIZE, MAX_N_GRAM_SIZE + 1):
                k_gram_series_for_one = pd.Series(generate_ngrams(sentence, n_gram_size))
                k_gram_series = k_gram_series.append(k_gram_series_for_one, ignore_index=True)
    # print(k_gram_series)
    # k_gram_series = pd.Series(generate_ngrams(whole_text, K_GRAM))

    data_frame = pd.DataFrame({'text': k_gram_series})
    # print(data_frame.size)
    data_frame['tag'] = ABSTAIN
    training_set, test_set = train_test_split(data_frame, test_size=0.2)
    return training_set, test_set
    # print(data_frame) #now we have untagged df


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