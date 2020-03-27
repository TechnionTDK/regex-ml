# regex-ml
## What's this project about

<br>We try here to create a classifier that will tag references of the Bavli Talmud in a given text.
<br>The program receives a csv file as input, breaks it into sentences, and then breaks each sentence into n-grams of sizes 3 to 7 (can be changed).
<br>The classifier then will determine whether the n-gram is a reference or not.

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

## Structue of this project

<br>The project consists of the following files:
<br>label_functions – contains the labeling functions and their description.
<br>labeling_activation – contains the trainif of the machine.
<br>utility – contains utility function, such as text parsing.

## How it works

<br>How the Labeling Functions where decided? by perliminary manual overview of examples of references to the the Talmud Bavli.
<br>Why we chose n-gram format? seemed most adequate and allowed us to include different sizes of references.
<br>That since we aspire that the tagging will be as acurate as possible, therefore we go over different n-gram sizes.

## Project Process
<br>The process consisted of three steps:
<br>First, creating a labeled data set - prepaing the data set involved extraction of the text from a csv file, devidןng it into ngrams of different sizes, creating labeling functions and cleaning the resulting labels from unnecessary duplications which using different ngram sizes may have caused. 
<br>Second, using transformations on the tagged dataset to enlarge it - the transformation were based on replacing masachtot and masachtot chapter names.
<br>Third, training the classifier. 


