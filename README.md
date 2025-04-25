# Phishing Email Classification App with Redis

This project showcases a machine learning-powered application designed to identify phishing emails effectively. It consists of four key components:

1. **Model Training (train.py)**: Prepares the dataset, trains a classifier using TF-IDF vectorization combined with logistic regression, and saves the trained model.
2. **Model Validation (validate.py)**: Assesses the model's performance on a testing dataset, generating metrics like accuracy, precision, and recall.
3. **Model Serving (serve.py)**: Offers real-time phishing email detection via a FastAPI service. To optimize performance, Redis caching is employed for quick handling of repeat requests.
4. **Redis Utility (check_redis.py)**: Provides insight into the Redis cache by displaying the total cached entries and sample predictions.

---

## Project Structure

```plaintext
.
├── data/
│   └── phishing_emails.csv         # Phishing email dataset from Kaggle
├── phishing_model.pkl              # Serialized model file
├── train.py                        # Script for training the classifier
├── validate.py                     # Script for validating the model
├── serve.py                        # FastAPI-based prediction API
└── check_redis.py                  # Script to inspect Redis cache entries

## How to Use

### 1. Train the Model
Run the training script to process the dataset and generate the model file:

Usage
1. Training the Model
Run the training script to process the dataset and generate the model file:

python train.py
2. Validating the Model
Run the validation script to evaluate the model's performance:

python validate.py
3. Serving Predictions
Ensure Redis is running (see instructions below for Windows), then start the FastAPI server:

python serve.py
Access the API at http://localhost:8000 and send POST requests to the /predict endpoint with JSON payloads:

{
  "text": "Your email content here..."
}

4. Checking Redis

Use the check_redis.py script to inspect the Redis cache. This script displays the number of cached entries and the first five email texts along with their predictions:

python check_redis.py

API Usage
Send a POST request to http://localhost:8000/predict with the following JSON payload:

curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "todays floor meeting you may get a few pointed questions about today article about lays potential severance of $ 80 mm"
}'
The API responds with a JSON object containing:

prediction: The predicted class name (e.g., "Phishing Email" or "Safe Email").
probability: The confidence score of the prediction.
Example response:

{
  "prediction": "Safe Email",
  "probability": 0.7791625553383463
}