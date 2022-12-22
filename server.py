from service import FinancialIndex
from utils.stripe_funcs import hash_api_key, unhash_api_key, generate_api_key

import datetime, requests, os, argparse, subprocess, logging, json
from typing import BinaryIO, Union

from sentence_transformers import SentenceTransformer
import pandas as pd

import uvicorn
from fastapi import FastAPI, Query, Header, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse

from pymongo import MongoClient
import bson

from dotenv import load_dotenv

import stripe
stripe.api_key = "sk_test_51MHqP5B9KUi6tSIMD2D5ghlwIDt9Gb5goiwJVdFemCRWTCXwv8i05kWfIxRqwTwbK5hKYLxGCRJRf13z5m1ViHMA00T89FTJsL"
#stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
# stripe listen --forward-to=localhost:8000/webhook

logging.getLogger().setLevel(logging.INFO)
load_dotenv() 

api_client_map = {}

"Change to a production DB"
def initMongo():
    
    uri = os.getenv("MONGO_DB_URI")
    cert_path = os.path.expanduser(os.getenv("MONGO_DB_CERT_PATH"))
    client = MongoClient(uri,
                        tls=True,
                        tlsCertificateKeyFile=cert_path)
    db = client['NewsAnalysis']
    return db

app = FastAPI()

intramove_db = initMongo()

### Stripe end points ###

@app.post("/webhook")
async def webhook(request: Request, event: dict): # add async
    # Check that the webhook is from Stripe
 
    eventType = event["type"]
    if eventType == "checkout.session.completed":
        customer_api_key = generate_api_key()
        hashed_customer_api_key = hash_api_key(customer_api_key) # should map to customer
        api_client_map[hashed_customer_api_key] = event["data"]["object"]["customer"]
        
    elif eventType == "invoice.paid":
        print(f"Payment succeeded:")
    elif eventType == "invoice.payment_failed":
        print(f"Payment failed:")
    else:
        # Unhandled event type
        return HTTPException(status_code=400, detail="Unhandled event type")
    
    return {"status": "success"}

@app.get("/customers")
def customers():
    #print(stripe.Customer.list())
    print(api_client_map)
    #return JSONResponse({"text":"welcome to intramove.ai"})


@app.post("/checkout")
def create_checkout_session(product_id: str, quantity: int):
    try:
        # Create the checkout session
        productObject = stripe.Product.retrieve(product_id)
        price_id = productObject.default_price
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id, #"price_1MHrPPB9KUi6tSIMyOtZPVOG",
                    "quantity": quantity,
                }
            ],
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
            mode="payment",
            customer_creation='always'
        )
        return JSONResponse({"session_id": session})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### END POINTS ###
@app.get("/")
def home():
    return JSONResponse({"text":"welcome to intramove.ai"})

@app.post("/analyze/headline")
def analyzeHeadline(api_key: str = Header(None),
                    headline: str = Query(), 
                    datetime: str = Query(),
                    callback_url: str = Query()):
    
    "Validate API key"

    "Bill usage"

    "Store client and other info in mongo DB"

    document_embedding = initializedFinaIndex.encodeText(
        headline
    )
    scores, indices = initializedFinaIndex.index.search(document_embedding, 1)
    scores = scores.flatten()
    indices = indices.flatten()

    selectedDescriptor = initializedFinaIndex.final_descriptors[indices[0]]

    if selectedDescriptor.sign == "bull":
        score = float(scores[0])
    elif selectedDescriptor.sign == "bear":
        score = float(scores[0])*-1

    output_dict = {"text":headline,
                    "datetime": datetime,
                    "sign":selectedDescriptor.sign,
                    "indicator":selectedDescriptor.indicator,
                    "description":selectedDescriptor.description,
                    "score":score}
    
    
    "Ensure you're using production DB"
    intramove_db["headline"].insert_one(output_dict,)

    del output_dict["_id"]

    if not callback_url:
        return JSONResponse(output_dict)
    else:
        requests.post(
            callback_url,
            json=output_dict,
        )

### SETUP ###

def start():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--device",
        dest="device",
        type=str,
        required=True,
        help="Device to use.",
    )
    args = parser.parse_args()
    
    if not os.path.isdir("sentence_models") or len(os.listdir("sentence_models")) == 0:
        subprocess.call(["python", "download_sm.py"])

    initializedFinaIndex = FinancialIndex(device=args.device, load=True)

    start()
