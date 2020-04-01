# regex-ml

## What's this project about

<br>We try here to create a labeled data set which will contain short sequences of an input text, and determine which is a reference to the Babylonian Talmud and which is not.
<br>The program receives a csv file as input, breaks it into sentences, and then breaks each sentence into n-grams of sizes 3 to 7 (can be changed). Using Snorkel and Pandas Python libraries, it uses predecided (manually) labeling functions to label the n-grams. 
We use the labeled data to train a classifier that will eventually find references for any input. The classifier then will determine whether the n-gram is a reference or not.

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

## Resources
<br> https://www.snorkel.org/
<br> https://scikit-learn.org/
<br> https://jakevdp.github.io/PythonDataScienceHandbook/

## Project Process
<br>The process consisted of three steps:
<br>1. First, creating a labeled data set - preparing the data set involved extraction of the text from a csv file, deviding it by sentences into ngrams of different sizes, creating the labeling functions and labeling using Snorkel Majority Label Voter model. Also, it involved cleaning the resulting labels from unnecessary duplications which using different ngram sizes may have caused. 
<br>2. Second, using transformations on the tagged dataset to enlarge it - the transformation were based on replacing masachtot and masachtot chapter names.
<br>3. Third, training the classifier - training the classifier using the Logistic Regression linear model (scikit learn), with
the labeled data set we have created as input.

 ## Clarifications

<br>How the Labeling Functions where decided? by perliminary manual overview of examples of references to the the Babylonian Talmud.
<br>Why we chose n-gram format? seemed most adequate and allowed us to include different sizes of references. That since we aspire that the tagging will be as acurate as possible, therefore we go over different n-gram sizes.

## Files of this project

<br>The project consists of the following files:
<br>main - the main part of the project, includes the labeled data creation and training of the classifier
<br>labeled_function – contains the labeling functions and their description.
<br>transformation_functions - contains the transformation functions used to increase the labeled data set
<br>utility – contains utility functions such as text parsing.
<br>Data directory:
<br> - contains the analysis file - contains output analysis for every run, of functions coverage and classifier accuracy.
<br> - csvRes - name of expected input text in csv format. 
<br> - df_test.csv and df_train.csv - 30-70 split of labeled data used to train the classifier
<br> - labeled_data - outputed labeled data
<br>  - labeled_data_augmented.csv - outputed labeled data including additions of transformation functions. 
 
 ## How to use this project:
 
 <br> 1. download the project. 
 <br> 2. take the input file (Hebrew text of course) and turn it into CSV file,  name it "csvRes.csv" and put it in the Data directory.
 <br> 3. Set the following constants which appear in the utility file:
 <br>  - SAMPLE_SIZE : the number of rows to use from the csv file.
 <br>  - MIN_N_GRAM_SIZE and MAX_N_GRAM_SIZE : determines the range of n-gram sizes.
 <br>  - TRANSFORMATION_FACTOR : determines the number of transformation of each label which contains a masechet or masechet chapter  name. It needs to be between 0 and number of total masachtot/prakim.
 <br> - TEST_RATIO = 0.30 # how to split train and test datasets for the classifier training.
 <br> 4. run.
 <br> 5. check the analysis files 
 
 <br> For further explanation, check the Snorkel website mentioned under resources. Consider changing the labeling and transformation functions if see it fit.
 <br>The main function calls for several important functions which purpose is described thoroughly in the code.
 <br> good luck!
 
