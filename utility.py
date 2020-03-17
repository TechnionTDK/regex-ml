
import pandas as pd
import json

from sklearn.model_selection import train_test_split


######################################################################
#################             GLOBALS            #####################
######################################################################

''' Tags:  '''
ABSTAIN = -1
REF = 1
NO_REF = 0

''' Constants: '''
SAMPLE_SIZE = 3
K_GRAM = 6
MIN_N_GRAM_SIZE = 3
MAX_N_GRAM_SIZE = 7
TRANSFORMATION_FACTOR = 15

''' Strings arrays containing "Masachtot"&"Prakim" names: '''
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

SHMOT_PRAKIM = ['מאימתי', 'היה קורא', 'מי שמתו', 'תפלת השחר', 'אין עומדין', 'כיצד מברכין', 'שלושה שאכלו', 'אלו דברים',
                'הרואה',
                'יציאות השבת', 'במה מדליקין', 'כירה', 'במה טומנין', 'במה בהמה', 'במה אשה', 'כלל גדול', 'המוציא יין',
                'אמר רבי עקיבא',
                'המצניע', 'הזורק', 'הבונה', 'האורג', 'שמנה שרצים', 'ואלו קשרים', 'כל כתבי', 'כל הכלים', 'מפנין',
                'רבי אליעזר דמילה', 'תולין',
                'נוטל', 'חבית', 'שואל', 'מי שהחשיך', 'מבוי שהוא גבוה', 'עושין פסים', 'בכל מערבין', 'מי שהוציאוהו',
                'כיצד מעברין', 'הדר',
                'חלון', 'כיצד משתתפין', 'כל גגות', 'המוצא תפילין', 'אור לארבעה עשר', 'כל שעה', 'אלו עוברין',
                'מקום שנהגו', 'תמיד נשחט',
                'אלו דברים', 'כיצד צולין', 'האשה', 'מי שהיה', 'ערבי פסחים', 'ארבעה ראשי שנים', 'אם אינן מכירין',
                'ראוהו בית דין', 'יום טוב',
                'שבעת ימים', 'בראשונה', 'אמר להם הממונה', 'טרף בקלפי', 'הוציאו לו', 'שני שעירי', 'בא לו כהן גדול',
                'יום הכיפורים', 'סוכה',
                'הישן תחת המטה', 'לולב הגזול', 'לולב וערבה', 'החליל', 'ביצה', 'יום טוב', 'אין צדין', 'המביא', 'משילין',
                'מאימתי', 'סדר תענית כיצד',
                'סדר תעניות אלו', 'בשלשה פרקים', 'מגילה נקראת', 'הקורא למפרע', 'הקורא עומד', 'בני העיר',
                'משקין בית השלחין', 'מי שהפך',
                'אלו מגלחין', 'הכל חייבין', 'אין דורשין', 'חומר בקודש', 'חמש עשרה נשים', 'כיצד', 'ארבעה אחין', 'החולץ',
                'רבן גמליאל',
                'הבא על יבמתו', 'אלמנה לכהן גדול', 'הערל', 'יש מותרות', 'האשה רבה', 'נושאין על האנוסה', 'מצות חליצה',
                'בית שמאי',
                'חרש שנשא', 'האשה שלום', 'האשה בתרא', 'בתולה נשאת', 'האשה שנתארמלה', 'אלו נערות', 'נערה שנתפתתה',
                'אף על פי',
                'מציאת האשה', 'המדיר', 'האשה שנפלו', 'הכותב לאשתו', 'מי שהיה נשוי', 'אלמנה ניזונת', 'הנושא את האשה',
                'שני דייני', 'כל כינויי',
                'ואלו מותרים', 'ארבעה נדרים', 'אין בין המודר', 'השותפין', 'הנודר מן המבושל', 'הנודר מן הירק',
                'קונם יין', 'רבי אליעזר', 'נערה המאורסה',
                'ואלו נדרים', 'כל כינויי נזירות', 'הריני נזיר', 'מי שאמר', 'מי שאמר', 'בית שמאי', 'שלשה מינין',
                'כהן גדול', 'שני נזירים', 'הכותים אין להם',
                'המקנא', 'היה מביא', 'היה נוטל', 'ארוסה', 'כשם שהמים', 'מי שקינא', 'אלו נאמרין', 'משוח מלחמה',
                'עגלה ערופה', 'המביא גט',
                'המביא גט', 'כל הגט', 'השולח', 'הניזקין', 'האומר', 'מי שאחזו', 'הזורק', 'המגרש', 'האשה נקנית',
                'האיש מקדש', 'האומר', 'עשרה יוחסין',
                'ארבעה אבות', 'כיצד הרגל', 'המניח', "שור שנגח ד' וה'", 'שור שנגח את הפרה', 'הכונס', 'מרובה', 'החובל',
                'הגוזל עצים', 'הגוזל ומאכיל',
                'שנים אוחזין', 'אלו מציאות', 'המפקיד', 'הזהב', 'איזהו נשך', 'השוכר את האומנין', 'השוכר את הפועלים',
                'השואל את הפרה',
                'המקבל שדה מחבירו', 'הבית והעליה', 'השותפין', 'לא יחפור', 'חזקת הבתים', 'המוכר את הבית',
                'המוכר את הספינה', 'המוכר פירות', 'בית כור',
                'יש נוחלין', 'מי שמת', 'גט פשוט', 'דיני ממונות בשלשה', 'כהן גדול', 'זה בורר', 'אחד דיני ממונות',
                'היו בודקין', 'נגמר הדין', 'ארבע מיתות',
                'בן סורר ומורה', 'הנשרפין', 'אלו הן הנחנקין', 'חלק', 'כיצד העדים', 'אלו הן הגולין', 'אלו הן הלוקין',
                'שבועות שתים', 'ידיעות הטומאה',
                'שבועות שתים', 'שבועת העדות', 'שבועת הפקדון', 'שבועת הדיינין', 'כל הנשבעים', 'ארבעה שומרין',
                'לפני אידיהן', 'אין מעמידין', 'כל הצלמים',
                'רבי ישמעאל', 'השוכר את הפועל', 'הורו בית דין', 'הורה כהן משיח', 'כהן משיח', 'כל הזבחים',
                'כל הזבחים שקבלו דמן', 'כל הפסולין',
                'בית שמאי', 'איזהו מקומן', 'קדשי קדשים', 'חטאת העוף', 'כל הזבחים', 'המזבח מקדש', 'כל התדיר', 'דם חטאת',
                'טבול יום', 'השוחט והמעלה',
                'פרת חטאת', 'כל המנחות', 'הקומץ את המנחה', 'הקומץ רבה', 'התכלת', 'כל המנחות באות מצה', 'רבי ישמעאל',
                'אלו מנחות נקמצות',
                'התודה היתה באה', 'כל קרבנות הציבור', 'שתי מדות', 'שתי הלחם', 'המנחות והנסכים', 'הרי עלי עשרון',
                'הכל שוחטין', 'השוחט', 'אלו טרפות',
                'בהמה המקשה', 'אותו ואת בנו', 'כסוי הדם', 'גיד הנשה', 'כל הבשר', 'העור והרוטב', 'הזרוע והלחיים',
                'ראשית הגז', 'שילוח הקן',
                'הלוקח עובר חמורו', 'הלוקח עובר פרתו', 'הלוקח בהמה', 'עד כמה', 'כל פסולי המוקדשין', 'על אלו מומין',
                'מומין אלו', 'יש בכור',
                'מעשר בהמה', 'הכל מעריכין', 'אין נערכין', 'יש בערכין', 'השג יד', 'האומר משקלי עלי', 'שום היתומים',
                'אין מקדישין', 'המקדיש שדהו',
                'המוכר שדהו', 'הכל ממירין', 'יש בקרבנות', 'אלו קדשים', 'ולד חטאת', 'כיצד מערימין', 'כל האסורין',
                'יש בקדשי מזבח', 'שלשים ושש',
                'ארבעה מחוסרי כפרה', 'אמרו לו', 'ספק אכל חלב', 'דם שחיטה', 'המביא אשם', 'קדשי קדשים', 'חטאת העוף',
                'ולד חטאת', 'קדשי מזבח',
                'הנהנה מן ההקדש', 'השליח שעשה', 'בשלשה מקומות', 'ראוהו אחיו', 'אמר להם הממונה', 'לא היו כופתין',
                'אמר להם הממונה', 'החלו עולים',
                'בזמן שכהן גדול', 'שמאי', 'כל היד', 'המפלת חתיכה', 'בנות כותים', 'יוצא דופן', 'בא סימן', 'דם הנדה',
                'הרואה כתם', 'האשה שהיא עושה',
                'תינוקת', 'אע"פ"ץ', 'המקבל']

######################################################################

def split_into_sentences(text):
    if ".)" in text: text = text.replace(".)", "<prd>)")
    sentences = text.split(".")
    text = text.replace("<prd>", ".")
    for s in sentences:
        s = s.replace("<prd>", ".")
    return sentences


def load_dataset():  # Load "Torat Emet" dataset
    df = pd.read_csv(r'data\csvRes.csv')
    data = ''
    k_gram_series = pd.Series()
    sentence_index = pd.Series()
    sentence_i = 0
    for x in range(SAMPLE_SIZE):
        data = df['text'][x]
        for sentence in split_into_sentences(data):
            for n_gram_size in range(MIN_N_GRAM_SIZE, MAX_N_GRAM_SIZE + 1):
                k_gram_series_for_one = pd.Series(generate_ngrams(sentence, n_gram_size))
                # print("supposed to print the size of k_gram_series_for_one")
                # print(len(k_gram_series_for_one.index))
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
    # print(data_frame)

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


######################################################################
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