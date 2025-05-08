import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import pickle
from sklearn.metrics import accuracy_score

# --- TRAINING PART ---

# Load the dataset
data = pd.read_csv("find_your_swiss_travel_personality.csv")
data.columns = data.columns.str.strip()  # Strip whitespace from all columns

# Prepare features and target
X = data.iloc[:, 1:-1].copy()  # All columns except the first (date) and last (holiday type)
X.columns = X.columns.str.strip()  # Strip again, just in case
y = data.iloc[:, -1]

# Encode the target labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Encode categorical features
categorical_columns = X.select_dtypes(include=['object']).columns
encoders = {}
for col in categorical_columns:
    encoder = LabelEncoder()
    X[col] = encoder.fit_transform(X[col])
    encoders[col] = encoder

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Test Accuracy: {accuracy:.2f}")

# Save the model, label encoder, feature encoders, and feature columns
with open("holiday_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)
with open("label_encoder.pkl", "wb") as encoder_file:
    pickle.dump(label_encoder, encoder_file)
with open("feature_encoders.pkl", "wb") as feature_encoders_file:
    pickle.dump(encoders, feature_encoders_file)
with open("feature_columns.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("Model, label encoder, feature encoders, and feature columns saved successfully!")

# --- PREDICTION PART ---

def predict_holiday_type(input_data):
    # Load the model and encoders
    with open("holiday_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    with open("label_encoder.pkl", "rb") as encoder_file:
        label_encoder = pickle.load(encoder_file)
    with open("feature_encoders.pkl", "rb") as feature_encoders_file:
        encoders = pickle.load(feature_encoders_file)
    with open("feature_columns.pkl", "rb") as f:
        feature_columns = pickle.load(f)

    # Convert input data to DataFrame if it's a dictionary
    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])

    # Strip whitespace from input columns
    input_data.columns = input_data.columns.str.strip()

    # Reindex input_data to match feature_columns, fill missing with empty string or suitable default
    input_data = input_data.reindex(columns=feature_columns)

    # Encode categorical features
    for col, encoder in encoders.items():
        if col in input_data.columns:
            # Fill NaN with a value that the encoder can handle (e.g., the most frequent or a default)
            input_data[col] = input_data[col].fillna(encoder.classes_[0])
            input_data[col] = encoder.transform(input_data[col])

    # Predict probabilities for each class
    probabilities = model.predict_proba(input_data)[0]  # Get the first (and only) row if predicting one sample

    # Get the class names
    class_labels = label_encoder.inverse_transform(range(len(probabilities)))

    # Find the predicted class and its probability
    predicted_index = probabilities.argmax()
    predicted_label = class_labels[predicted_index]
    predicted_probability = probabilities[predicted_index]

    # Create a dictionary of class probabilities (optional, for more detailed output)
    class_probabilities = {label: f"{prob*100:.1f}%" for label, prob in zip(class_labels, probabilities)}
    print(f"Predicted label: {predicted_label}, Probability: {predicted_probability:.2f}")
    print(f"Class probabilities: {class_probabilities}")
    

    return predicted_label, predicted_probability, class_probabilities
