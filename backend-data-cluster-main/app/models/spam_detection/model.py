import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

class SpamDetection():
  def __init__(self):
    # Initialize the SpamDetection class, set the model path, and perform setup and model loading
    self.model_path = 'app/models/spam_detection/trained_model.pkl'
    self.setup()
    self.load_model()

  def setup(self):
    # Read data, preprocess, and prepare training data
    df = pd.read_csv('app/models/spam_detection/traindata.csv')
    df = df.where((pd.notnull(df)), '')
    # Convert category labels from 'spam'/'ham' to binary
    df.loc[df['Category'] == 'spam', 'Category'] = 0
    df.loc[df['Category'] == 'ham', 'Category'] = 1
    X = df['Message']
    Y = df['Category']
    # Split the data into training and test sets, ignoring the test set here
    X_train, _, Y_train, _ = train_test_split(
        X, Y, test_size=0.2, random_state=3)
    # Initialize TF-IDF vectorizer for text feature extraction
    self.feature_extraction = TfidfVectorizer(
        min_df=1, stop_words='english', lowercase=True)
    # Transform the training data to feature vectors
    self.X_train_features = self.feature_extraction.fit_transform(X_train)
    self.Y_train = Y_train.astype('int')

  def load_model(self):
    # Load the pre-trained model or train a new one if not found
    try:
        self.model = joblib.load(self.model_path)
    except FileNotFoundError:
        self.train_model()

  def train_model(self):
    # Train a logistic regression model with the prepared data
    self.model = LogisticRegression()
    self.model.fit(self.X_train_features, self.Y_train)
    # Save the trained model
    joblib.dump(self.model, self.model_path)

  def is_spam(self, review):
    # Predict if a given review text is spam
    review = [review]
    input_features = self.feature_extraction.transform(review)
    prediction = self.model.predict(input_features)
    return True if prediction[0] == 1 else False