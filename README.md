# regex-ml
## What's this project about

We try here to create a classifier that will tag references of the Bavli Talmud in a given text.
The program receives a csv file as input, breaks it into sentences, and then breaks each sentence into n-grams of sizes 3 to 7 (can be changed). The classifier then will determine whether the n-gram is a reference of not.

## Installation guidelines

In order to run this project, you'll need python version 3.7.1.
Install the requirements from the requirements file:
```
pip install -r requirements.txt
```
If you run into truble with torch installation, try install it manually, then install the requirements:
```
pip install torch===1.1.0 torchvision===0.3.0 -f https://download.pytorch.org/whl/torch_stable.html

pip install -r requirements.txt
```
## Structue of this project

The project consists of the following files:
label_functions – contains the labeling functions and their description.
labeling_activation – contains the trainif of the machine.
utility – contains utility function, such as text parsing.

## How it's works

How the Labeling Functions where decided?
Why we chose n-gram format?
We aspire that the tagging will be as acurate as possible, therefore we go over different n-gram sizes.
