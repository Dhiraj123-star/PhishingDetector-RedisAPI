import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

def main():
    # load dataset 
    df = pd.read_csv("data/Phishing_Email.csv")

    # assume dataset has columns "text" and "label"

    X = df["Email Text"].fillna("")
    y = df["Email Type"]

    # split the dataset into training and testing sets

    X_train,X_test,y_train,y_test=train_test_split(
        X,y,test_size=0.2,random_state=42
    )

    # create pipeline with TF-IDF and Logistic Regression

    pipeline = Pipeline(
        [
            ("tfidf",TfidfVectorizer(stop_words="english")),
            ("clf",LogisticRegression(solver="liblinear")),
        ]
    )
    #train the model
    pipeline.fit(X_train,y_train)

    # save the trained model to a file

    joblib.dump(pipeline,"phishing_model.pkl")
    print("Model trained and saved as phishing_model.pkl")

if __name__=="__main__":
    main()