
import pandas as pd
import json

from sklearn.model_selection import train_test_split


ABSTAIN = -1

# tag
REF = 1

# not tag

NO_REF = 0

SAMPLE_SIZE = 2
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
    sentence_index = pd.Series()
    sentence_i = 0
    for x in range(len(df.index)):
        data = df['text'][x]
        for sentence in split_into_sentences(data):
            for n_gram_size in range(MIN_N_GRAM_SIZE, MAX_N_GRAM_SIZE + 1):
                k_gram_series_for_one = pd.Series(generate_ngrams(sentence, n_gram_size))
                print("supposed to print the size of k_gram_series_for_one")
                print(len(k_gram_series_for_one.index))
                # check whether to add ".index" or something else for size of a Series
                sentence_index_temp = pd.Series([sentence_i for x in range(len(k_gram_series_for_one.index))])
                sentence_index = sentence_index.append(sentence_index_temp, ignore_index=True)

                k_gram_series = k_gram_series.append(k_gram_series_for_one, ignore_index=True)
            sentence_i = sentence_i+1



    # k_gram_series = pd.Series(generate_ngrams(whole_text, K_GRAM))

    # adding column to dfwith ngram indices(regardless of their sentences), for filtering uses
    # in run_lf function, in cases where a kgram and k+1gram were tagged, and we want to delete the kgram line
    n_gram_id = pd.Series(range(0, len(k_gram_series.index)))


    data_frame = pd.DataFrame({'text': k_gram_series, 'sentence_index': sentence_index, 'n_gram_id': n_gram_id})
    # print(data_frame.size)
    data_frame['tag'] = ABSTAIN

    # TODO: REMOVE PRINT FROM HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    print(data_frame)

    training_set, test_set = train_test_split(data_frame, test_size=0.0001)
    return training_set, test_set, sentence_i
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


# this function was run-once- to create a list of all the name of the chapters in the talmud bavli
# if you wish to run them again, put all relevant files from git inside project directory
def collect_talmud_chapters_names():
    chapter_names=[]
    for i in range(1,38):
        fname="talmudbavli-"+str(i)+"-packages.json"
        #print(fname.strip())
        collect_talmud_chapters_from_file(fname.strip(),chapter_names)
    print(chapter_names)

# this function extract for every masecet (each file) its chapters names
def collect_talmud_chapters_from_file(file,chapters_list):

    with open(file, encoding='utf-8') as pyhthon_file:
        data = json.loads(pyhthon_file.read())
        counter = 0
        for line in data['subjects']:
            counter += 1
            if counter == 1:
                continue
            name = line['rdfs:label']
            flag_dash=False
            flag_skipped_spaces=False
            extract=""
            for i in range(len(name)):
                if name[i] == "-":
                    flag_dash = True
                    continue
                if flag_dash is False:
                    continue
                if name[i]==" " and flag_dash and flag_skipped_spaces is False:
                    continue
                flag_skipped_spaces=True
                if flag_dash:
                        extract+=name[i]
            chapters_list.append(extract)