# LOCAL MODULES
from service import FinancialIndex
from utils.stripe_funcs import hash_api_key, unhash_api_key, generate_api_key
from models import StripeCustomer
# NATIVE LIBS
import datetime, requests, os, argparse, subprocess, logging, json
from typing import BinaryIO, Union

# ML & ENV
from sentence_transformers import SentenceTransformer
import pandas as pd
from dotenv import load_dotenv

# SERVER
import uvicorn
from fastapi import FastAPI, Query, Header, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse

# DATABASE
from pymongo import MongoClient

# PAYMENT & AUTH
import stripe

logging.getLogger().setLevel(logging.INFO)
load_dotenv() 

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
# stripe listen --forward-to=localhost:8000/webhook
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

    """signature = request.headers["Stripe-Signature"]
    try:
        event = stripe.Webhook.construct_event(
            request.body, signature, stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HTTPException(status_code=400, detail="Invalid signature")"""
 
    eventType = event["type"]
    if eventType == "checkout.session.completed":
        customer_id = event["data"]["object"]["customer"]
        customer_email = event["data"]["object"]["customer_details"]["email"]
        customer_api_key = generate_api_key()
        
        hashed_customer_api_key = hash_api_key(customer_api_key) # should map to customer

        customerObj = StripeCustomer(hash_api_key, 500, True,customer_id,customer_email)
        api_client_map[hashed_customer_api_key] = customerObj
        print(customer_api_key)
        # Mechanism to email key to client
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
    print(stripe.Customer.list())
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
def analyzeHeadline(api_key: str = Header(),
                    headline: str = Query(), 
                    datetime: str = Query(),
                    callback_url: str = Query()):
    
    "Validate API key"
    if not api_key:
        return {"error":"API key is missing."}
    
    hashed_api_key = hash_api_key(api_key)

    if hashed_api_key in api_client_map.keys():
        customerObj = api_client_map[hashed_api_key]
        if not customerObj.active:
            return {"error":"recharge is required"}
        if customerObj.calls == 0:
            customerObj.active = False
            api_client_map[hashed_api_key] = customerObj
            return {"error":"recharge is required"}
        customerObj.calls -=1 
        api_client_map[hashed_api_key] = customerObj
    else:
        return {"error": "API key is invalid."}

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
    #intramove_db["headline"].insert_one(output_dict,)

    #del output_dict["_id"]

    return JSONResponse(output_dict)
    
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
