import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.calibration import CalibratedClassifierCV
import joblib
import numpy as np
import os

# Load synthetic dataset
# df = pd.read_csv('backend/real_world_symptoms_synthetic.csv')
df = pd.read_csv('real_world_symptoms_synthetic_merged.csv')

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Keep only columns that are numeric or the target
symptom_cols = [col for col in df.columns if col == 'prognosis' or np.issubdtype(df[col].dtype, np.number)]
df = df[symptom_cols]

# Fill missing values with 0 (assume absence of symptom)
df = df.fillna(0)

# Remove prognosis classes with fewer than 2 samples
prognosis_counts = df['prognosis'].value_counts()
rare_classes = prognosis_counts[prognosis_counts < 2].index.tolist()
if rare_classes:
    print('Removing prognosis classes with <2 samples:', rare_classes)
    df = df[~df['prognosis'].isin(rare_classes)]
    print('New shape after removing rare classes:', df.shape)

print('Final training data shape:', df.shape)

X = df.drop('prognosis', axis=1)
y = df['prognosis']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train model
base_clf = RandomForestClassifier(n_estimators=100, random_state=42)
calibrated_clf = CalibratedClassifierCV(base_clf, method='isotonic', cv=3)
calibrated_clf.fit(X_train, y_train)

# Save calibrated model
model_path = os.path.join(os.path.dirname(__file__), 'public_symptom_model.pkl')
joblib.dump(calibrated_clf, model_path)

# Evaluate on test set
y_pred = calibrated_clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred, zero_division=0)

print('Test Accuracy:', acc)
print('Test Precision:', prec)
print('Test Recall:', rec)
print('Test F1-score:', f1)
print('Confusion Matrix:\n', cm)
print('Classification Report:\n', report)

# Cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_acc = cross_val_score(calibrated_clf, X, y, cv=cv, scoring='accuracy')
cv_f1 = cross_val_score(calibrated_clf, X, y, cv=cv, scoring='f1_weighted')
print('Cross-validated Accuracy: %.3f ± %.3f' % (cv_acc.mean(), cv_acc.std()))
print('Cross-validated F1-score: %.3f ± %.3f' % (cv_f1.mean(), cv_f1.std()))

# Check probability outputs
probs = calibrated_clf.predict_proba(X_test)
print('First row of probabilities:', probs[0])
print('Sum of first row:', np.sum(probs[0]))

# Save metrics report
to_save = f"""
Test Accuracy: {acc:.4f}
Test Precision: {prec:.4f}
Test Recall: {rec:.4f}
Test F1-score: {f1:.4f}
Confusion Matrix:\n{cm}
Classification Report:\n{report}
Cross-validated Accuracy: {cv_acc.mean():.4f} ± {cv_acc.std():.4f}
Cross-validated F1-score: {cv_f1.mean():.4f} ± {cv_f1.std():.4f}
First row of probabilities: {probs[0]}
Sum of first row: {np.sum(probs[0])}
"""
with open('model_metrics_report.txt', 'w') as f:
    f.write(to_save)

print('Training feature columns:', list(X.columns)) 