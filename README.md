# regex-ml

*A tool for extracting refrences to the Babylonian Talmud from a given corpus, using weak supervision machine learning methods.*

## Table of Contents:
- [About](#about)
- [Installation](#installation)
- [Resources](#resources)
- [The Project Process](#process)
- [Q&A](#qa)
- [Files](#files)
- [How to use](#howto)
- [Key Functions](#functions)
- [Conclusions](#conclusions)

<a name="about"/>

## About this project:

<br>This project is testing whether using machine learning tools might be useful in tasks of information tagging. It is a part of a larger project, “The Jewish Book Closet”, and focuses on tagging references of Hebrew sources - in this case, the Babylonian Talmud.
<br>
<br>In the past, regular expressions were used for the task of finding these references, but they have proven difficult to work with, especially with Hebrew sources, and therefore a machine learning approach was tested.
<br>One of the most difficult steps when working with machine learning is the creation of a large enough data set for the machine to learn from. Our purpose was to create that data set using weak supervision machine learning methods. 

<br>This tool creates a labeled data set which will contain short sequences of an input text, and determine which sequence is a [reference to the Babylonian Talmud](#qa) and which is not: 
<br>The program receives a CSV file as input, breaks it into sentences, and then breaks each sentence into sequences in a range of sizes (can be changed). Using [Snorkel](https://www.snorkel.org/) and [Pandas](https://pandas.pydata.org/) Python libraries, it uses predecided (manually) labeling functions to label the sequences and create the tagged data set.
<br>


<br> For detailed information about the project, please visit the [wiki](https://github.com/TechnionTDK/regex-ml/wiki/Introduction) page 📚📜.

<a name="installation"/>

## Installation guidelines

<br>In order to run this project, you'll need python version 3.7.1.
<br>Install the requirements from the requirements file:
```
pip install -r requirements.txt
```
If you run in trouble with torch installation, try installing it manually, then install the requirements:
```
pip install torch===1.1.0 torchvision===0.3.0 -f https://download.pytorch.org/whl/torch_stable.html

pip install -r requirements.txt
```

<a name="resources"/>

## Resources
<br> https://www.snorkel.org/
<br> https://scikit-learn.org/
<br> https://jakevdp.github.io/PythonDataScienceHandbook/
<br> https://pandas.pydata.org/

<a name="process"/>

## Project Process
<br>The process consisted of three steps:
- First, creating a labeled data set - preparing the data set involved extraction of the text from a csv file, deviding it by sentences into ngrams of different sizes, creating the labeling functions and labeling using Snorkel Majority Label Voter model. Also, it involved cleaning the resulting labels from unnecessary duplications which using different ngram sizes may have caused. 
- Second, using transformations on the tagged dataset to enlarge it - the transformation were based on replacing masachtot and masachtot chapter names.
- Third, training the classifier - training the classifier using the Logistic Regression linear model (scikit learn), with
the labeled data set we have created as input.

<a name="qa"/>

 ## Q&A
 
- Q: **What is a reference to the Babylonian Talmud?**
<br>A: Here is an example:
 >**":ובפרק תינוקת (ברכות דף ס"ט)"**

- Q: **How were the Labeling Functions decided?**
<br>A: By perliminary manual overview of examples of references to the the Babylonian Talmud.
<br> more info on that you can find in the [wiki](https://github.com/TechnionTDK/regex-ml/wiki/Introduction).
- Q: **Why was the n-gram format chosen?**
<br>A: Seemed most adequate and allowed us to include different sizes of references. That since we aspire that the tagging will be as acurate as possible, therefore we go over different n-gram sizes.

*More clarifications will be added in the future if necessary*

<a name="files"/>

## Important files of this project

<br>The project consists mainly of the following files:
<br>-**Root directory:**
<br>--->[main.py](main.py) - the main part of the project, includes the labeled data creation and training of the classifier
<br>--->[labeled_function.py](labeled_function.py) – contains the labeling functions and their description.
<br>--->[transformation_functions.py](transformation_function.py) - contains the transformation functions used to increase the labeled data set
<br>--->[utility.py](utility.py) – contains utility functions such as text parsing.
<br>-**Data directory:**
<br>--->[analysis file](data/analysis.txt) - contains output analysis for every run, of functions coverage and classifier accuracy.
<br>--->[csvRes](data/csvRes.csv) - name of expected input text in csv format. 
<br>--->[df_test.csv](data/df_test.csv) and df_train.csv - 30-70 split of labeled data used to train the classifier
<br>--->[labeled_data](data/labeled_data.csv) - outputed labeled data
<br>--->[labeled_data_augmented.csv](data/labeled_data_augmented.csv) - outputed labeled data including additions of transformation functions. 

 <a name="howto"/>
 
 ## How to use this project:
 
1. 🍴 Fork or 👯 Clone this repo to your local machine.
2. Take the input file (Hebrew text of course) and turn it into CSV file,  name it "csvRes.csv" and put it in the Data directory.
3. Set the following constants which appear in the [utility file](utility.py) -
* <b>SAMPLE_SIZE</b> : the number of rows to use from the csv file.
* <b>MIN_N_GRAM_SIZE</b> and <b>MAX_N_GRAM_SIZE</b> : determines the range of n-gram sizes.
* <b>TRANSFORMATION_FACTOR</b> : determines the number of transformation of each label which contains a masechet or masechet chapter  name. It needs to be between 0 and number of total masachtot/prakim.
* <b>TEST_RATIO</b> = 0.30 : how to split train and test datasets for the classifier training.
4. Run [main.py](main.py) .
5. Check the results at the [analysis file](data/analysis.txt) and explore 🔨 

 <a name="functions"/>
 
 ## Important functions
 
 <br>In [main.py](main.py):
* load_labeled_data - extracts ngrams from the csv input file
* apply_lf_on_data - appplies the labeling functions on the data set and tags them
* apply_tf_on_data - applies the transformation functions on the labeled data set
* train_model - trains the classifier and outputs results
 
  <a name="conclusions"/>
 
 ## Conclusions
 
<br>The working process showed that the task at hand was much easier than it was using only regular expressions, especially when dealing with Hebrew sources. Most importantly, it resulted in a large tagged data set, which would have been impossible to create manually.
<br>To test if the data set is satisfactory for a machine to learn from, we've created a basic classifier using the data set and then checked it on a small test set. 
<br>
<br>The next step is to take the data set this tool creates, and train a classifier that will tag any input text.
<br>We believe that with further understanding of existing tools in machine learning it will be possible to achieve even better and more meaningful results.

---
<br>For further explanation, please check out the [wiki](https://github.com/TechnionTDK/regex-ml/wiki/Introduction) page.
<br>Also, check out the [Snorkel website](https://www.snorkel.org/) mentioned under resources. Consider changing the labeling and transformation functions if see it fit.
<br>The main function calls for several important functions which purpose is described thoroughly in the code.
<br>
<br> good luck!
 
