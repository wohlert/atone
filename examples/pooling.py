"""
pooling

This is an example pipeline demonstrating the creation
of a classifier based on trial-wise pooling along
with a support vector machine classifier on the data.

This particular solution will yield an accuracy of
0.69 on the competition.
"""


import numpy as np
import agnosia.io as io
import agnosia.preprocessing as pre
from agnosia.features import pool
from agnosia.pipeline import Pipeline

np.random.seed(8829)

folder = "../data"

# Load data and metadata
X_train, X_test, y_train, y_test = io.load_subjects(folder, False)
sfreq, tmin, _ = io.load_meta(folder)
onset = int(abs(sfreq*tmin))

# Create pipeline
pipeline = Pipeline()
pipeline.add(pre.cut_samples, [onset])
pipeline.add(pool)

# Run pipeline
X_train = pipeline.run(X_train)
X_test = pipeline.run(X_test)

# Create classifier
from sklearn.svm import SVC
model = SVC()
model.fit(X_train, y_train.ravel())

# Create submission
prediction = model.predict(X_test)
io.create_submission(y_test.ravel(), prediction, "submission_pooling.csv")
