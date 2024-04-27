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
| subject_id | has_disease(0/1)| phenotypes (list)   |
+------------+-----------------+---------------------+
"""
def randomForest(df):
  # One-hot encode the phenotypes
  mlb = MultiLabelBinarizer()
  encoded_phenotypes = pd.DataFrame(mlb.fit_transform(df['phenotypes']), columns=mlb.classes_, index=df.index)
  df = df.drop('phenotypes', axis=1).join(encoded_phenotypes)

  # Convert boolean to int
  df['has_disease'] = df['has_disease'].astype(int)

  # Split the data into a training set and a test set
  X_train, X_test, y_train, y_test = train_test_split(df.drop('has_disease', axis=1), df['has_disease'], test_size=0.1, random_state=42)

  # Train a Random Forest classifier
  clf = RandomForestClassifier(n_estimators=100, random_state=42)
  clf.fit(X_train, y_train)

  # Make predictions on the test set
  y_pred = clf.predict(X_test)

  # Print a classification report
  logger.info(classification_report(y_test, y_pred))

  # Create a DataFrame with subject_id and y_pred
  results_df = pd.DataFrame({
    'subject_id': X_test['subject_id'],
    'y_pred': y_pred
  })

  return results_df