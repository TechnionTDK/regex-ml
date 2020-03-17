import pandas as pd
import labeled_function
import transformation_function
from snorkel.labeling import MajorityLabelVoter
import utility

# from utils import load_torat_emet_dataset

from snorkel.labeling import PandasLFApplier
from snorkel.augmentation import PandasTFApplier

from snorkel.labeling import LFAnalysis
from snorkel.analysis import get_label_buckets

from snorkel.augmentation import RandomPolicy

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

SAMPLE_SIZE = 3
K_GRAM = 6
MIN_N_GRAM_SIZE = 3
MAX_N_GRAM_SIZE = 7



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
    dev.to_csv(r'data\dev.csv', index=False)
    return dev


def run_lf_on_data():
    print("")
    print("Labeling Functions:")
    df_train, df_test, sentences_number = utility.load_torat_emet_data()
    df_dev = pd.read_csv('dev_22.12.csv')
    df_train.to_csv(r'data\df_train.csv',
                    index=False)

    #df_dev = create_devset(df_train)
    # print(f"Dev REF frequency: {100 * (df_dev.tag.values == REF).mean():.1f}%")

    #TODO: when creating test and dev, use split function
    #TODO: -to devide 50/50 between them
    Y_dev = df_dev.tag.values
    #TODO:add validation set and dev set
    """
    lfs = [labeled_function.if_parenthesis, labeled_function.if_perek, labeled_function.if_begins_with_perek,
           labeled_function.if_daf, labeled_function.if_mashechet,
           labeled_function.if_amod, labeled_function.if_begin_or_end_of_perek, labeled_function.check_mishna, 
           labeled_function.check_legal_paren_num]
    """
    lfs = [labeled_function.masechet_then_parans, labeled_function.perek_then_parans, labeled_function.perek_and_sham,
           labeled_function.mashechet_and_sham, labeled_function.daf_in_parntes, labeled_function.no_double_parans,
           labeled_function.no_mishna]
    applier = PandasLFApplier(lfs=lfs)
    print("-Applying the labeling functions...")
    l_train = applier.apply(df=df_train)
    l_dev = applier.apply(df=df_dev)

    coverage_masechet_then_parans, coverage_perek_then_parans, coverage_perek_and_sham, \
    coverage_mashechet_and_sham, coverage_daf_in_parntes , coverage_no_double_parans, coverage_no_mishna = (l_train != ABSTAIN).mean(axis=0)
    print("")
    print(":::::::::::::::::::|LF Coverage|:::::::::::::::::::::::")
    print(f"::coverage_masechet_then_parans: {coverage_masechet_then_parans * 100:.1f}%")
    print(f"::coverage_perek_then_parans: {coverage_perek_then_parans * 100:.1f}%")
   # print(f"::coverage_if_begins_with_perek: {coverage_if_begins_with_perek * 100:.1f}%")
    print(f"::coverage_perek_and_sham: {coverage_perek_and_sham * 100:.1f}%")
    print(f"::coverage_mashechet_and_sham: {coverage_mashechet_and_sham * 100:.1f}%")
    print(f"::coverage_daf_in_parntes: {coverage_daf_in_parntes * 100:.1f}%")
    print(f"::coverage_no_double_parans: {coverage_no_double_parans * 100:.1f}%")
    print(f"::coverage_no_mishna: {coverage_no_mishna * 100:.1f}%")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    #label_model = LabelModel(cardinality=2, verbose=True)
    #label_model.fit(L_train=l_train, n_epochs=500, lr=0.001, log_freq=100, seed=123)

    # print("=======")
    # print(" summary of l_train ")
    # print(LFAnalysis(L=l_train, lfs=lfs).lf_summary())
    # print(" summary of l_dev - only tagged ")
    # print(LFAnalysis(L=l_dev, lfs=lfs).lf_summary(Y=Y_dev))


# part c - see what lf mislabeled and compare with other lfs
    buckets = get_label_buckets(Y_dev, l_dev[:, 1])
#    print(" indexes of ngram where lf mislabeled ")
 #   print(df_dev.iloc[buckets[(NO_REF, REF)]])

 #   print(" check what this lf caught - check if_mashecet - will be 10 samples")
 #   print(df_train.iloc[l_train[:, 3] ==REF].sample(10, random_state=1))

    print("-Applying the MajorityLabelVoter...")
    majority_model = MajorityLabelVoter()
    preds_train = majority_model.predict(L=l_train)

    #TODO: compare this model with other model
    # print(" === result ===")
    # print (preds_train)
    #for debuging, exe preds train to file
    #savetxt('preds_t',preds_train, delimiter=',')

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

    print("-Dropping the extra columns...")
    df_train = df_train.drop(["sentence_index","n_gram_id"],axis=1)
    print("DONE")
    return df_train

def run_tf_on_data(df_train):
    print("")
    print("Transformation Functions:")
    tfs = [transformation_function.change_perek, transformation_function.change_masechet]
    random_policy = RandomPolicy(
        len(tfs), sequence_length=2, n_per_original=5, keep_original=True
    )
    print("-Applying the transformation functions...")
    tf_applier = PandasTFApplier(tfs, random_policy)
    df_train_augmented = tf_applier.apply(df_train)
    # Y_train_augmented = df_train_augmented["tag"].values
    print("DONE")
    return df_train_augmented

def main():
    #load_torat_emet_data()
    #df_train, df_test = load_torat_emet_data()
    #dev = create_devset(df_train)

    df_train = run_lf_on_data()
    df_train.to_csv(r'data\labeled_data.csv', index=False)
    df_augmented = run_tf_on_data(df_train)
    df_augmented.to_csv(r'data\labeled_data_augmented.csv', index=False)

    print(f"Original training set size: {len(df_train)}")
    print(f"Augmented training set size: {len(df_augmented)}")

    df = pd.read_csv('csvRes.csv')
    print("check for us!!!!")
    print(len(df.index))

if __name__ == "__main__":
    main()