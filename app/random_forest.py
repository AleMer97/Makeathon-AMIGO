import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
df format:
+------------+-----------------+---------------------+
| subjectId  | isSick (0/1)    | phenotypes (list)   |
+------------+-----------------+---------------------+
"""
def randomForestA(df):
  # One-hot encode the phenotypes
  mlb = MultiLabelBinarizer()
  encoded_phenotypes = pd.DataFrame(mlb.fit_transform(df['phenotypes']), columns=mlb.classes_, index=df.index)
  df = df.drop('phenotypes', axis=1).join(encoded_phenotypes)

  # Convert boolean to int
  df['isSick'] = df['isSick'].astype(int)

  # Split the data into a training set and a test set
  X_train, X_test, y_train, y_test = train_test_split(df.drop(['isSick', 'icdFirstLetter'], axis=1), df['isSick'], test_size=0.1, random_state=42)

  # Train a Random Forest classifier
  clf = RandomForestClassifier(n_estimators=100, random_state=42)
  clf.fit(X_train, y_train)

  # Make predictions on the test set
  y_pred = clf.predict(X_test)

  # Print a classification report
  logger.info(f"Results Task A {classification_report(y_test, y_pred)}")

  # Create a DataFrame with subjectId and y_pred
  results_df = pd.DataFrame({
    'subjectId': X_test['subjectId'],
    'y_pred': y_pred
  })

  return results_df

def randomForestB(df):
  # One-hot encode the phenotypes
  mlb = MultiLabelBinarizer()
  encoded_phenotypes = pd.DataFrame(mlb.fit_transform(df['phenotypes']), columns=mlb.classes_, index=df.index)
  df = df.drop('phenotypes', axis=1).join(encoded_phenotypes)

  # Split the data into a training set and a test set
  X_train, X_test, y_train, y_test = train_test_split(df.drop(['isSick', 'icdFirstLetter'], axis=1), df['icdFirstLetter'], test_size=0.1, random_state=42)

  # Train a Random Forest classifier
  clf = RandomForestClassifier(n_estimators=100, random_state=42)
  clf.fit(X_train, y_train)

  # Make predictions on the test set
  y_pred = clf.predict(X_test)

  # Print a classification report
  logger.info(f"Results Task B {classification_report(y_test, y_pred)}")

  # Create a DataFrame with subjectId and y_pred
  results_df = pd.DataFrame({
    'subjectId': X_test['subjectId'],
    'y_pred': y_pred
  })

  return results_df