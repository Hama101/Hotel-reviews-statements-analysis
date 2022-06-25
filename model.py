'''
    this code is responsible for loading the model this file will run once when the server starts
'''
import asyncio
import warnings
warnings.filterwarnings('ignore')
import os
import pandas as pd
import matplotlib.pyplot as plt
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import Pipeline
import joblib


def save_pipeline_model(model):
    print("Saving Model...")
    joblib.dump(model, 'model/model.joblib')
    print("****done saving the model ****")

#load the model from the \model folder
def load_model():
    print("Loading Model...")
    model = joblib.load('model/model.joblib')
    print("****done loading the model ****")
    return model

def train_model():
    # Local directory
    Reviewdata1 = pd.read_csv('data\data-set-train.csv')
    Reviewdata2 = pd.read_csv('data\hotel-reviews.csv')
    Reviewdata = pd.concat([Reviewdata1, Reviewdata2])
    #Data Credit - https://www.kaggle.com/anu0012/hotel-review/data

    print("Loading Model...")
    Reviewdata.describe().transpose()

    ### Checking Missing values in the Data Set and printing the Percentage for Missing Values for Each Columns ###
    count = Reviewdata.isnull().sum().sort_values(ascending=False)
    percentage = ((Reviewdata.isnull().sum()/len(Reviewdata)*100)).sort_values(ascending=False)
    missing_data = pd.concat([count, percentage], axis=1, keys=['Count','Percentage'])

    #Removing columns
    Reviewdata.drop(columns = ['User_ID', 'Browser_Used', 'Device_Used'], inplace = True)

    # Apply first level cleaning
    #This function converts to lower-case, removes square bracket, removes numbers and punctuation
    def text_clean_1(text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text

    cleaned1 = lambda x: text_clean_1(x)

    # Let's take a look at the updated text
    Reviewdata['cleaned_description'] = pd.DataFrame(Reviewdata.Description.apply(cleaned1))
    # Reviewdata.head(10)

    # Apply a second round of cleaning
    def text_clean_2(text):
        text = re.sub('[‘’“”…]', '', text)
        text = re.sub('\n', '', text)
        return text

    cleaned2 = lambda x: text_clean_2(x)

    # Let's take a look at the updated text
    Reviewdata['cleaned_description_new'] = pd.DataFrame(Reviewdata['cleaned_description'].apply(cleaned2))
    # Reviewdata.head(10)
    
    Independent_var = Reviewdata.cleaned_description_new
    Dependent_var = Reviewdata.Is_Response

    IV_train, IV_test, DV_train, DV_test = train_test_split(Independent_var, Dependent_var, test_size = 0.1, random_state = 225)

    tvec = TfidfVectorizer()
    clf2 = LogisticRegression(solver = "lbfgs")

    model = Pipeline([('vectorizer',tvec),('classifier',clf2)])

    model.fit(IV_train, DV_train)

    predictions = model.predict(IV_test)

    confusion_matrix(predictions, DV_test)

    print("****done loading the model ****")
    # save the model to \model
    save_pipeline_model(model)
    return model


async def load_model_async():
    return await asyncio.to_thread(load_model)


if __name__ == '__main__':
    train_model()
    load_model()

