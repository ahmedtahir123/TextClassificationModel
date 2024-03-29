# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BqYNVOrgPVPeDx7MPVwXTa7P1LG0bdrD
"""

import numpy as np
import re
import pickle
import nltk
from nltk.corpus import stopwords
from sklearn.datasets import load_files
nltk.download('stopwords')

from zipfile import ZipFile
file_name='txt_sentoken.zip'
with ZipFile(file_name,'r') as zip:
  zip.extractall()

#load dataset
review=load_files('txt_sentoken/')
X,Y=review.data,review.target
#store as Pickle File
with open ('X.pickle','wb') as f:
  pickle.dump(X,f)
with open ('Y.pickle','wb') as f:
  pickle.dump(Y,f)
#read from pickle file or unpickling
with open ('X.pickle','rb') as f:
  X=pickle.load(f)

with open ('Y.pickle','rb') as f:
  Y=pickle.load(f)

#creating the preprocess corpus 

corpus=[]
for i in range(0,len(X)):
  data=re.sub(r'\W',' ',str(X[i]))
  data=data.lower()
  data=re.sub(r'\s+[a-z]\s+',' ',data)
  data=re.sub(r'^[a-z]\s+',' ',data)
  data=re.sub(r'\s+',' ',data)
  corpus.append(data)

#creating Bow Model
# from sklearn.feature_extraction.text import CountVectorizer
# vectorizer=CountVectorizer(max_features=2000,min_df=3,max_df=0.6,stop_words=stopwords.words('english'))
# X=vectorizer.fit_transform(corpus).toarray()

#converting Bow Model into Tfid model
# from sklearn.feature_extraction.text import TfidfTransformer
# transformer=TfidfTransformer()
# X=transformer.fit_transform(X).toarray()

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer=TfidfVectorizer(max_features=2000,min_df=3,max_df=0.6,stop_words=stopwords.words('english'))
X=vectorizer.fit_transform(corpus).toarray()

#CREATING the  test and train SET
from sklearn.model_selection import train_test_split
text_train,text_test,sent_train,sent_test=train_test_split(X,Y,test_size=0.2,random_state=0)

#training our classifier
from sklearn.linear_model import LogisticRegression
classifier=LogisticRegression()
classifier.fit(text_train,sent_train)
with open ('classifier.pickle','wb') as f:
  pickle.dump(classifier,f)
with open ('Tfidfmodel.pickle','wb') as f:
  pickle.dump(vectorizer,f)

# Testing Model Performance
sent_pred=classifier.predict(text_test)
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(sent_test,sent_pred)
(cm[0][0]+cm[1][1])/4

with open ('classifier.pickle','rb') as f:
  clf=pickle.load(f)
with open ('Tfidfmodel.pickle','rb') as f:
  tfidf=pickle.load(f)
sample=['bad']
sample=tfidf.transform(sample).toarray()
print(clf.predict(sample))