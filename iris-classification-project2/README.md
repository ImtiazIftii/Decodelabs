# Iris Classification with K-Nearest Neighbors

Project 2 of the DecodeLabs AI Industrial Training Kit — a supervised learning classification task using the classic Iris dataset.

## Overview

This project builds a K-Nearest Neighbors (KNN) classifier to predict flower species (setosa, versicolor, virginica) from four measurements: sepal length, sepal width, petal length, and petal width. It covers the full ML pipeline: data exploration, preprocessing, training, evaluation, and experimentation.

## Dataset

- **Source:** Iris dataset (150 samples, 3 balanced classes, 4 numeric features)
- **Location:** `data/iris.csv`

## How to Run

1. Clone this repository and navigate to this project folder.
2. Create and activate a virtual environment:
python -m venv venv
source venv/Scripts/activate # Windows (Git Bash)

3. Install dependencies:
pip install -r requirements.txt

4. Launch Jupyter Notebook:
python -m notebook

5. Open `notebooks/iris_classification.ipynb` and run all cells from top to bottom.

## Approach

- Split data into train/test sets before scaling, to prevent data leakage.
- Standardized features using `StandardScaler` (fit on training data only).
- Trained a `KNeighborsClassifier` and evaluated using accuracy, a confusion matrix, and a full precision/recall/F1 classification report.
- Ran additional experiments: testing sensitivity to K, testing performance using only the two most predictive features, and testing performance on a harder subset of the data (removing the easily-separable `setosa` class).

## Results

Achieved 100% accuracy on the full 3-class test set. Further experimentation confirmed the model's strong performance is driven by clean, well-separated classes in the dataset — and that difficulty increases, as expected, when the easier class is removed, revealing genuine overlap between `versicolor` and `virginica`.

## Author

Built as part of the DecodeLabs Industrial Training Kit, Batch 2026.