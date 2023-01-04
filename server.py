# LOCAL MODULES
from service import FinancialIndex
from utils.stripe_funcs import generate_api_key
from models import StripeCustomer
from utils.chunker import advanced_chunker

# NATIVE LIBS
import os, argparse, subprocess, logging, requests
from bson import ObjectId

# ML & ENV
from dotenv import load_dotenv
import faiss

# SERVER
import uvicorn
from fastapi import FastAPI, Query, Header, HTTPException, Request
from fastapi.responses import HTMLResponse

from fastapi.responses import JSONResponse

# DATABASE
from pymongo import MongoClient

# PAYMENT & AUTH
import stripe

logging.getLogger().setLevel(logging.INFO)
load_dotenv(".env")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
# stripe listen --forward-to=localhost:443/webhook
# stripe listen --forward-to=https://api.intramove.ai:443/webhook

package_credits_count_map = {"prod_N2ndwwdkNjVThi": 100, 
                             "prod_N3UFpCDcp0Hisv": 100}

product_id_to_name_map = {
    "prod_N2ndwwdkNjVThi": "headlines-100",
    "prod_N3UFpCDcp0Hisv": "articles-100",
}

def initMongo():
    uri = os.getenv("MONGO_DB_URI")
    cert_path = os.path.expanduser(os.getenv("MONGO_DB_CERT_PATH"))
    client = MongoClient(uri, tls=True, tlsCertificateKeyFile=cert_path)
    db = client["intramovedb"]
    return db


app = FastAPI()

intramove_db = initMongo()

### Stripe end points ###

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
                    "price": price_id,  # "price_1MHrPPB9KUi6tSIMyOtZPVOG",
                    "quantity": quantity,
                }
            ],
            success_url="https://api.intramove.ai:443/success",
            cancel_url="https://api.intramove.ai:443/failure",
            mode="payment",
            customer_creation="always",
            automatic_tax={
                "enabled": True,
            },
            metadata={
                "product_id": product_id,
                "quantity": quantity,
                "number_of_api_credits": package_credits_count_map[product_id],
            },
        )
        return JSONResponse({"session_id": session})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhook", include_in_schema=False)
async def webhook(request: Request, event: dict):  # add async
    # Verify the webhook signature
    try:
        payload = await request.body()
        sig_header = request.headers["stripe-signature"]
        stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except ValueError as e:
        # Invalid payload
        return HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HTTPException(status_code=400, detail="Invalid signature")

    eventType = event["type"]
    if eventType == "checkout.session.completed":

        stripe_customer_id = event["data"]["object"]["customer"]
        customer_email = event["data"]["object"]["customer_details"]["email"]
        customer_name = event["data"]["object"]["customer_details"]["name"]
        customer_postal_code = event["data"]["object"]["customer_details"]["address"][
            "postal_code"
        ]
        customer_country = event["data"]["object"]["customer_details"]["address"][
            "country"
        ]
        customer_total_spend = event["data"]["object"]["amount_total"]

        event_metadata = event["data"]["object"]["metadata"]
        quantity = event_metadata["quantity"]
        number_of_api_credits = event_metadata["number_of_api_credits"]
        product_id = event_metadata["product_id"]
        product_name = product_id_to_name_map[product_id]

        number_of_api_credits = int(number_of_api_credits) * int(quantity)
        assert type(number_of_api_credits) == int, "Variable must be an integer."

        query = {"name": customer_name, "email": customer_email}

        # Find the customer
        customer = intramove_db["customers"].find_one(query)
        if customer:
            # Define the update
            if product_name == "headlines-100":
                update = {
                    "$set": {
                        "headline_credits_available": customer[
                            "headline_credits_available"
                        ]
                        + number_of_api_credits,
                        "headline_active": True,
                        "number_of_payments": customer["number_of_payments"] + 1,
                        "total_spend": customer["total_spend"] + customer_total_spend,
                    }
                }
            elif product_name == "articles-100":
                update = {
                    "$set": {
                        "article_credits_available": customer[
                            "article_credits_available"
                        ]
                        + number_of_api_credits,
                        "article_active": True,
                        "number_of_payments": customer["number_of_payments"] + 1,
                        "total_spend": customer["total_spend"] + customer_total_spend,
                    }
                }

            # Update the customer
            result = intramove_db["customers"].update_one(query, update)
            if result.acknowledged:
                logging.info("Customer was updated successfully")
        else:
            customer_api_key = generate_api_key()

            if product_name == "headlines-100":
                customerObj = StripeCustomer(
                    api_key=customer_api_key,
                    headline_credits_available=number_of_api_credits,
                    article_credits_available=0,
                    number_of_payments=1,
                    headline_active=True,
                    article_active=False,
                    stripe_customer_id=stripe_customer_id,
                    email=customer_email,
                    name=customer_name,
                    postal_code=customer_postal_code,
                    country=customer_country,
                    total_spend=int(customer_total_spend) * int(quantity),
                    headline_credits_consumed=0,
                    article_credits_consumed=0,
                )
            elif product_name == "articles-100":
                customerObj = StripeCustomer(
                    api_key=customer_api_key,
                    headline_credits_available=0,
                    article_credits_available=number_of_api_credits,
                    number_of_payments=1,
                    headline_active=False,
                    article_active=True,
                    stripe_customer_id=stripe_customer_id,
                    email=customer_email,
                    name=customer_name,
                    postal_code=customer_postal_code,
                    country=customer_country,
                    total_spend=int(customer_total_spend) * int(quantity),
                    headline_credits_consumed=0,
                    article_credits_consumed=0,
                )

            result = intramove_db["customers"].insert_one(customerObj.generate_dict())
            if result.acknowledged:
                logging.info("Customer was inserted successfully")

        # Mechanism to email key to client
    elif eventType == "invoice.paid":
        logging.info(f"Payment succeeded:")
    elif eventType == "invoice.payment_failed":
        logging.info(f"Payment failed:")
    else:
        # Unhandled event type
        return HTTPException(status_code=400, detail="Unhandled event type")

    return {"status": "success"}


@app.get("/client_api_key")
def client_api_key(client_id: str):
    query = {"_id": ObjectId(client_id)}
    customer = intramove_db["customers"].find_one(query)
    if customer:
        return JSONResponse({"api_key": customer["api_key"]})
    return None


@app.get("/client_id")
def client_id(email: str, name: str):
    query = {"email": email, "name": name}
    customer = intramove_db["customers"].find_one(query)
    if customer:
        return JSONResponse({"client_id": str(customer["_id"])})
    return None


@app.get("/credits_available")
def credits_available(api_key: str, product_name: str):
    query = {"api_key": api_key}
    customer = intramove_db["customers"].find_one(query)
    if customer:
        if product_name == "headlines-100":
            return JSONResponse(
                {"headline_credits_available": customer["headline_credits_available"]}
            )
        elif product_name == "articles-100":
            return JSONResponse(
                {"article_credits_available": customer["article_credits_available"]}
            )
    return None


@app.get("/credits_consumed")
def credits_consumed(api_key: str, product_name: str):
    query = {"api_key": api_key}
    customer = intramove_db["customers"].find_one(query)
    if customer:
        if product_name == "headlines-100":
            return JSONResponse(
                {"headline_credits_consumed": customer["headline_credits_consumed"]}
            )
        elif product_name == "articles-100":
            return JSONResponse(
                {"article_credits_consumed": customer["article_credits_consumed"]}
            )
    return None


@app.get("/status")
def status(api_key: str, product_name: str):
    query = {"api_key": api_key}
    customer = intramove_db["customers"].find_one(query)
    if customer:
        if product_name == "headlines-100":
            return JSONResponse(
                {"status": "Active" if customer["headline_active"] else "Inactive"}
            )
        elif product_name == "articles-100":
            return JSONResponse(
                {"status": "Active" if customer["article_active"] else "Inactive"}
            )
    return None


@app.get("/success")
def success():
    return HTMLResponse(
        """<html>
  <head>
    <style>
      h1 {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
      }
    </style>
  </head>
  <body>
    <h1>Purchase successful!</h1>
  </body>
</html>"""
    )


@app.get("/failure")
def failure():
    return HTMLResponse(
        """<html>
  <head>
    <style>
      h1 {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
      }
    </style>
  </head>
  <body>
    <h1>Purchase failed.</h1>
  </body>
</html>"""
    )


### AI SERVICE ###


@app.post("/analyze/headline")
def analyzeHeadline(
    api_key: str = Header(),
    headline: str = Query(),
    date: str = Query(),
    callback_url: str = Query(),
):

    "Validate API key"
    if not api_key:
        return {"error": "API key is empty."}

    query = {"api_key": api_key}

    # Find the customer
    customer = intramove_db["customers"].find_one(query)

    if not customer:
        return JSONResponse({"error": "API key entered is invalid."})

    if customer["headline_credits_available"] == 0:
        update = {"$set": {"headline_active": False}}
        # Update the customer
        result = intramove_db["customers"].update_one(query, update)
        if result.acknowledged:
            logging.info("Customer set to headline-inactive.")
        return JSONResponse({"error": "recharge is required"})

    customer_db_id = customer["_id"]

    if not customer:
        return JSONResponse({"error": "API key is missing or is not valid."})

    if not customer["headline_active"]:
        return JSONResponse({"error": "headline recharge is required."})

    update = {
        "$inc": {"headline_credits_available": -1, "headline_credits_consumed": 1}
    }
    # Update the customer
    intramove_db["customers"].update_one(query, update)

    "Store client and other info in mongo DB"
    document_embedding = initializedFinaIndex.encodeText(headline)
    scores, indices = initializedFinaIndex.index.search(document_embedding, 1)
    scores = scores.flatten()
    indices = indices.flatten()

    selectedDescriptor = initializedFinaIndex.final_descriptors[indices[0]]

    if selectedDescriptor.sign == "bull":
        score = float(scores[0])
    elif selectedDescriptor.sign == "bear":
        score = float(scores[0]) * -1

    output_dict = {
        "text": headline,
        "date": date,
        "sign": selectedDescriptor.sign,
        "indicator": selectedDescriptor.indicator,
        "description": selectedDescriptor.description,
        "score": score,
        "api_key": api_key,
        "customer_id": customer_db_id,
    }

    intramove_db["headlines"].insert_one(
        output_dict,
    )

    del output_dict["_id"]
    del output_dict["api_key"]
    del output_dict["customer_id"]

    if not callback_url:
        return JSONResponse(output_dict)
    else:
        requests.post(
            callback_url,
            json=output_dict,
        )


@app.post("/analyze/article")
def analyzeArticle(
    api_key: str = Header(),
    article: str = Query(),
    date: str = Query(),
    callback_url: str = Query(),
):

    "Validate API key"
    if not api_key:
        return {"error": "API key is empty."}

    query = {"api_key": api_key}

    # Find the customer
    customer = intramove_db["customers"].find_one(query)

    if not customer:
        return JSONResponse({"error": "API key entered is invalid."})

    if customer["article_credits_available"] == 0:
        update = {"$set": {"article_active": False}}
        # Update the customer
        result = intramove_db["customers"].update_one(query, update)
        if result.acknowledged:
            logging.info("Customer set to article_inactive.")
        return JSONResponse({"error": "Article recharge is required"})

    customer_db_id = customer["_id"]

    if not customer:
        return JSONResponse({"error": "API key is missing or is not valid."})

    if not customer["article_active"]:
        return JSONResponse({"error": "Article recharge is required."})

    update = {"$inc": {"article_credits_available": -1, "article_credits_consumed": 1}}
    # Update the customer
    intramove_db["customers"].update_one(query, update)

    chunks = advanced_chunker(article)
    chunks_analysis = []  # text:results
    average_score = 0

    document_embeddings = initializedFinaIndex.encodeChunks(chunks)
    faiss.normalize_L2(document_embeddings)

    distances, indices = initializedFinaIndex.index.search(document_embeddings, 1)

    max_scores = distances.flatten()
    indices = indices.flatten()

    selectedDescriptors = [
        initializedFinaIndex.final_descriptors[index] for index in indices
    ]

    for descriptor_index, selectedDescriptor in enumerate(selectedDescriptors):
        if selectedDescriptor.sign == "bull":
            average_score += max_scores[descriptor_index]
            score = float(max_scores[descriptor_index])
        elif selectedDescriptor.sign == "bear":
            average_score -= max_scores[descriptor_index]
            score = float(max_scores[descriptor_index])*-1

        if score > 0.6:
            chunk_analysis = {
                "chunk": chunks[descriptor_index],
                "sign": selectedDescriptor.sign,
                "indicator": selectedDescriptor.indicator,
                "description": selectedDescriptor.description,
                "score": score,
            }

            chunks_analysis.append(chunk_analysis)

    output_dict = {
        "chunks": chunks_analysis,
        "average_score": average_score,
        "average_sign": "bull" if average_score > 0 else "bear",
        "date": date,
        "api_key": api_key,
        "customer_id": customer_db_id,
    }

    intramove_db["articles"].insert_one(
        output_dict,
    )

    del output_dict["_id"]
    del output_dict["api_key"]
    del output_dict["customer_id"]

    if not callback_url:
        return JSONResponse(output_dict)
    else:
        requests.post(
            callback_url,
            json=output_dict,
        )


### SETUP ###


def start():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=443,
        log_level="info",
        ssl_keyfile=os.getenv("SSL_KEYFILE_PATH"),
        ssl_certfile=os.getenv("SSL_CERTIFICATE_PATH"),
    )
    """import subprocess

    # Set the path to the Uvicorn executable
    uvicorn_path = os.getenv("UVICORN_PATH") 

    # Set the path to the SSL/TLS certificate and private key files
    ssl_keyfile = os.getenv("SSL_KEYFILE_PATH")
    ssl_certfile = os.getenv("SSL_CERTIFICATE_PATH")

    # Set the command to run Uvicorn using authbind
    command = ['sudo', uvicorn_path, 'server:app', '--host', '0.0.0.0', '--port', '443', '--log-level', 'info', '--ssl-keyfile', ssl_keyfile, '--ssl-certfile', ssl_certfile]

    # Run the command
    subprocess.run(command)"""


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
