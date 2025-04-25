import asyncio
import json
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
import redis.asyncio as redis

# create an asynchronous Redis client 
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

# load the trained model by synchronously
model = joblib.load("phishing_model.pkl")

app = FastAPI()

# define the request and response data models

class PredictionRequest(BaseModel):
    text:str

class PredictionResponse(BaseModel):
    prediction:str
    probability:float


@app.post("/predict",response_model=PredictionResponse)
async def predict_email(data:PredictionRequest):
    # use the email text as a cache key
    cache_key = f"prediction:{data.text}"
    cached = await redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    # run model inference in a thread to avoid the blocking the event loop
    pred = await asyncio.to_thread(model.predict,[data.text])
    prob = await asyncio.to_thread(lambda: model.predict_proba([data.text])[0].max())

    result = {
        "prediction":str(pred[0]),
        "probability":float(prob)
    }

    # cache the result for 30 minutes (1800 seconds)

    await redis_client.setex(cache_key,1800,json.dumps(result))
    return result

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)