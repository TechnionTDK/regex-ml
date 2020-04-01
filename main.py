"""
Our Talmud Bavli regex-ml project.
Created by: Rotem, Shaked, Liraz and Ariel
"""
import pandas as pd
import datetime
## Snorkel:
from snorkel.labeling import MajorityLabelVoter
from snorkel.labeling import PandasLFApplier
from snorkel.augmentation import PandasTFApplier
from snorkel.labeling import LFAnalysis
from snorkel.augmentation import RandomPolicy
## sklearn:
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
## Locals:
import labeled_function
import transformation_function
import utility
from utility import TRANSFORMATION_FACTOR
from utility import ABSTAIN
from utility import TEST_RATIO


'''
def csv_to_string():
    df = pd.read_csv('csvRes.csv')
    data =''
    print(df.shape[0])
    print(df.size)
    #TODO: or real run change 50 to df.shape[0]
    for x in range(SAMPLE_SIZE):
        data+= df['text'][x]
    #print(data)
    return data
'''

def print_analysis(l_train,lfs):
    """
    Prints LF's coverage and statistics
    """
    coverage_masechet_then_parans, coverage_perek_then_parans, \
    coverage_daf_in_parntes, coverage_no_double_parans, coverage_no_mishna = (
                l_train != ABSTAIN).mean(axis=0)
    txt_file = open(r"data/analysis.txt", "a+")
    txt_file.write("\n\n")
    txt_file.write('Analysis for date ['+str(datetime.datetime.now())+']: \n')
    txt_file.write('[SAMPLE_SIZE: ' + str(utility.SAMPLE_SIZE) + '] \n')
    txt_file.write('[TRANSFORMATION_FACTOR: ' + str(TRANSFORMATION_FACTOR) + '] \n')
    txt_file.write("\n\n")
    txt_file.write(":::::::::::::::::::::::::::|LFs Coverage|::::::::::::::::::::::::::::::::\n")
    txt_file.write(f"coverage_masechet_then_parans: {coverage_masechet_then_parans * 100:.1f}%\n")
    txt_file.write(f"coverage_perek_then_parans: {coverage_perek_then_parans * 100:.1f}%\n")
    txt_file.write(f"coverage_daf_in_parntes: {coverage_daf_in_parntes * 100:.1f}%\n")
    txt_file.write(f"coverage_no_double_parans: {coverage_no_double_parans * 100:.1f}%\n")
    txt_file.write(f"coverage_no_mishna: {coverage_no_mishna * 100:.1f}%\n")
    txt_file.write(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")
    txt_file.write(":::::::::::::::::::::::|LFs Summary - l_train|:::::::::::::::::::::::::::\n")
    txt_file.write(LFAnalysis(L=l_train, lfs=lfs).lf_summary().to_string())
    txt_file.write("\n")
    txt_file.write(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")
    # txt_file.write("::::::::::::::::::::::::|LFs Summary - l_dev|::::::::::::::::::::::::::::\n")
    # txt_file.write(LFAnalysis(L=l_dev, lfs=lfs).lf_summary(Y=Y_dev).to_string())
    # txt_file.write("\n")
    # txt_file.write(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")
    txt_file.close()

def log_print(str):
    """
    Print to the console AND append data/analysis.txt
    """
    print(str)
    txt_file = open(r"data/analysis.txt", "a+")
    txt_file.write(str)
    txt_file.write("\n")
    txt_file.close()


def create_devset(train_set):
    """
    This function is for creting
    """
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
    dev.to_csv(r'data\dev.csv', index=False)
    return dev

def create_labeled_data():
    """
    Creates the labeled data set.
    First we load the unlabeled data with utility.py
    Then applying labeling and transformation functions.
    """
    df_train, sentences_number = utility.load_dataset()

    df_dev = pd.read_csv(r'data\dev_22.12.csv')
    df_train.to_csv(r'data\df_train.csv', index=False)

    df_train_labeled = apply_lf_on_data(df_train,df_dev,sentences_number)
    df_train_labeled.to_csv(r'data\labeled_data.csv', index=False)

    augmented = apply_tf_on_data(df_train_labeled)

    # Splitting to test and train:
    df_train_augmented, df_test = train_test_split(augmented, test_size=TEST_RATIO)
    df_test.to_csv(r'data\df_test.csv', index=False)
    df_train_augmented.to_csv(r'data\labeled_data_augmented.csv', index=False)

    return df_train_labeled,df_train_augmented,df_test

def load_labeled_data(to_create=False):
    """
    Loads the data, if 'to_create' is on then actually create the data.
    If not, then load it from the 'data' folder.
    """
    if to_create:
        df_train_labeled,df_train_augmented,df_test = create_labeled_data()
    else:
        df_test = pd.read_csv(r'data\df_test.csv')
        df_train_labeled = pd.read_csv(r'data\labeled_data.csv')
        df_train_augmented = pd.read_csv(r'data\labeled_data_augmented.csv')
    return df_train_labeled,df_train_augmented,df_test


def apply_lf_on_data(df_train,df_dev,sentences_number):
    """
    This function apply the labeling functions (from labeled_function.py)
    on given train data frame.
    Other parameters: df_dev (for further developing the LFs) and sentences_number for inner use.
    Return the train df with the tagging.
    """
    print("")
    print("Labeling Functions:")

    # Y_dev = df_dev.tag.values
    lfs = [labeled_function.masechet_then_parans, labeled_function.perek_then_parans,
           labeled_function.daf_in_parntes, labeled_function.no_double_parans,
           labeled_function.no_mishna]
    applier = PandasLFApplier(lfs=lfs)

    print("-Applying the labeling functions...")
    l_train = applier.apply(df=df_train)
    # l_dev = applier.apply(df=df_dev)

    print_analysis(l_train,lfs)

    print("-Applying the MajorityLabelVoter...")
    majority_model = MajorityLabelVoter()
    preds_train = majority_model.predict(L=l_train)

    #put predicted labels in df train
    print("-Removing unnecessary n-grams...")
    df_train['tag'] = preds_train
    for i in range(sentences_number):
        df_filter_by_sentences = df_train.loc[df_train['sentence_index'] == i]
        df_filter = df_filter_by_sentences.loc[df_filter_by_sentences['tag'] == 1]
        # this section handles cases of positively tagged ngram within a bigger positively tagged ngram, and removes it.
        for row_checked in df_filter.index:
            for row_other in df_filter.index:
                if df_filter['n_gram_id'][row_checked] != df_filter['n_gram_id'][row_other] and \
                        df_filter['text'][row_checked] in df_filter['text'][row_other]:
                    df_train = df_train[df_train.n_gram_id != df_filter['n_gram_id'][row_checked]]
                    break

    print("-Dropping the abstained and extra columns...")
    df_train = df_train.drop(["sentence_index","n_gram_id"],axis=1)
    df_train = df_train[df_train['tag'] != ABSTAIN]
    print("DONE")
    return df_train

def apply_tf_on_data(df_train):
    """
    Here we apply the transformation functions (from transformation_function.py)
    on the given train data frame.
    Return the enlarged data frame.
    """
    print("")
    print("Transformation Functions:")
    tfs = [transformation_function.change_perek, transformation_function.change_masechet]
    random_policy = RandomPolicy(
        len(tfs), sequence_length=len(tfs), n_per_original=TRANSFORMATION_FACTOR, keep_original=True
    )
    print("-Applying ["+str(len(tfs))+"] transformation functions with factor ["+str(TRANSFORMATION_FACTOR)+"] ...")
    tf_applier = PandasTFApplier(tfs, random_policy)
    df_train_augmented = tf_applier.apply(df_train)
    # Y_train_augmented = df_train_augmented["tag"].values
    print("DONE")
    return df_train_augmented

def train_model(df_train,df_test):
    """
    In this function the model training is happening.
    It takes train and test data frames, and
    return classifier, X_test (the text) and y_test (the labels)
    """
    vectorizer = CountVectorizer(ngram_range=(1, 1))
    X_train = vectorizer.fit_transform(df_train.text.tolist())
    y_train = df_train.tag.values
    X_test = vectorizer.transform(df_test.text.tolist())
    y_test = df_test.tag.values

    clf = LogisticRegression(solver="lbfgs")
    clf.fit(X=X_train, y=y_train)

    return clf,X_test,y_test


def main():
    """
    Simple use-case for this project.
    """
    print("Initializing data...")
    df_train_labeled,df_train_augmented,df_test = load_labeled_data(True)

    log_print("::::::::::::::::::::::::::::::|Results|::::::::::::::::::::::::::::::::::")
    log_print(f"Test set: ({TEST_RATIO}% of Train data)\nsize [{len(df_test)}] , # References [{len(df_test[df_test['tag']==1].index)}] , # No-References [{len(df_test[df_test['tag']==0].index)}]")
    log_print(f"Original training set: \nsize [{len(df_train_labeled)}] , # References [{len(df_train_labeled[df_train_labeled['tag']==1].index)}] , # No-References [{len(df_train_labeled[df_train_labeled['tag']==0].index)}]")
    log_print(f"Augmented training set: \nsize [{len(df_train_augmented)}] , # References [{len(df_train_augmented[df_train_augmented['tag']==1].index)}] , # No-References [{len(df_train_augmented[df_train_augmented['tag']==0].index)}]")


    print("Original set based training...")
    clf,X_test,y_test = train_model(df_train_labeled, df_test)
    log_print(f"Test Accuracy: {clf.score(X=X_test, y=y_test) * 100:.1f}%")
    print("Augmented set based training...")
    clf,X_test,y_test = train_model(df_train_augmented, df_test)
    log_print(f"Test Accuracy: {clf.score(X=X_test, y=y_test) * 100:.1f}%")


    print("DONE")





if __name__ == "__main__":
    main()