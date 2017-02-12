import sys
from sklearn import ensemble, linear_model, svm
import scipy.sparse as sp
import pickle
import numpy as np
import math

with open('model0', 'r') as m:
    m0 = pickle.load(m)
with open('model1','r') as m:
    m1 = pickle.load(m)

with open('vectorizer_11100','r') as v:
    vectorizer_11100 = pickle.load(v)
with open('vectorizer_112000','r') as v:
    vectorizer_112000 = pickle.load(v)
with open('vectorizer_224000','r') as v:
    vectorizer_224000 = pickle.load(v)
with open('vectorizer_22500','r') as v:
    vectorizer_22500 = pickle.load(v)
with open('vectorizer_33100','r') as v:
    vectorizer_33100 = pickle.load(v)
with open('vectorizer_332000','r') as v:
    vectorizer_332000 = pickle.load(v)
with open('vectorizer_441000','r') as v:
    vectorizer_441000 = pickle.load(v)
with open('vectorizer_551000','r') as v:
    vectorizer_551000 = pickle.load(v)

with open('ch2_11100', 'r') as ch:
    ch2_11100 = pickle.load(ch)
with open('ch2_112000', 'r') as ch:
    ch2_112000 = pickle.load(ch)
with open('ch2_224000', 'r') as ch:
    ch2_224000 = pickle.load(ch)
with open('ch2_22500', 'r') as ch:
    ch2_22500 = pickle.load(ch)
with open('ch2_33100','r') as ch:
    ch2_33100 = pickle.load(ch)
with open('ch2_332000','r') as ch:
    ch2_332000 = pickle.load(ch)
with open('ch2_441000','r') as ch:
    ch2_441000 = pickle.load(ch)
with open('ch2_551000','r') as ch:
    ch2_551000 = pickle.load(ch)

test = []
test.append("you fucker you fucking suck dick you cuntwaffle.")
test.append("I love you, you goddess of the sun.")

def vectorize(t):
    y1 = vectorizer_112000.transform(t)
    y1 = ch2_112000.transform(y1)
    y2 = vectorizer_224000.transform(t)
    y2 = ch2_224000.transform(y2)
    y3 = vectorizer_33100.transform(t)
    y3 = ch2_33100.transform(y3)
    y4 = vectorizer_441000.transform(t)
    y4 = ch2_441000.transform(y4)
    y5 = vectorizer_551000.transform(t)
    y5 = ch2_551000.transform(y5)
    y6 = vectorizer_332000.transform(t)
    y6 = ch2_332000.transform(y6)
    y7 = vectorizer_11100.transform(t)
    y7 = ch2_11100.transform(y7)
    y8 = vectorizer_22500.transform(t)
    y8 = ch2_22500.transform(y8)

    y = sp.hstack([y1,y2,y3,y4,y5,y6,y7,y8])
    return y

def predict(x):
    t = []
    t.append(x)
    vec = vectorize(t)
    model0 = m0.predict_proba(vec)
    model1 = m1.predict_proba(vec)
    
    prediction = model0*0.4 + model1*0.6
    return prediction[0][1]

if __name__ == "__main__":
    print predict(sys.argv[1])
