# LOCAL MODULES
from service import FinancialIndex
from utils.stripe_funcs import hash_api_key, generate_api_key, unhash_api_key
from models import StripeCustomer

# NATIVE LIBS
import os, argparse, subprocess, logging

# ML & ENV
from dotenv import load_dotenv

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
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
# stripe listen --forward-to=localhost:8000/webhook
api_client_map = {}
client_cache = []
package_creditscount_map = {"prod_N1vFZNiYNDhyM3": 5}
"Change to a production DB"


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
            success_url="http://localhost:8000/success",
            cancel_url="http://localhost:8000/failure",
            mode="payment",
            customer_creation="always",
            metadata={
                "product_id": product_id,
                "quantity": quantity,
                "number_of_api_credits": package_creditscount_map[product_id],
            },
        )
        return JSONResponse({"session_id": session})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhook")
async def webhook(request: Request, event: dict):  # add async
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

        number_of_api_credits = int(number_of_api_credits) * int(quantity)
        assert type(number_of_api_credits) == int, "Variable must be an integer."

        query = {"name": customer_name, "email": customer_email}

        # Find the customer
        customer = intramove_db["customers"].find_one(query)
        if customer:
            # Define the update
            update = {
                "$set": {
                    "credits": customer["credits"] + number_of_api_credits,
                    "active": True,
                    "number_of_payments": customer["number_of_payments"] + 1,
                    "total_spend": customer["total_spend"] + customer_total_spend,
                    "credits_consumed": customer["credits_consumed"]
                    + number_of_api_credits,
                }
            }

            # Update the customer
            result = intramove_db["customers"].update_one(query, update)
            if result.acknowledged:
                print("Customer was updated successfully")
        else:
            customer_api_key = generate_api_key()
            customerObj = StripeCustomer(
                api_key=customer_api_key,
                credits=number_of_api_credits,
                number_of_payments=1,
                active=True,
                stripe_customer_id=stripe_customer_id,
                email=customer_email,
                name=customer_name,
                postal_code=customer_postal_code,
                country=customer_country,
                total_spend=int(customer_total_spend) * int(quantity),
                credits_consumed=int(number_of_api_credits),
            )

            result = intramove_db["customers"].insert_one(customerObj.generate_dict())
            if result.acknowledged:
                print("Customer was inserted successfully")

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
    # return JSONResponse({"text":"welcome to intramove.ai"})


@app.get("/clientkey")
def clientkey(email: str, name: str):
    for customerObj in client_cache:
        if email == customerObj.customer_email and name == customerObj.customer_name:
            return {"api_key": customerObj.api_key}
    return {"error": "No API key found."}


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
    datetime: str = Query(),
    callback_url: str = Query(),
):

    "Validate API key"
    if not api_key:
        return {"error": "API key is empty."}

    query = {"api_key": api_key}

    # Find the customer
    customer = intramove_db["customers"].find_one(query)

    if not customer:
        return {"error": "API key is missing or is not valid."}

    if not customer["active"]:
        return {"error": "recharge is required."}

    if customer["credits"] == 0:
        update = {"$set": {"active": False}}
        # Update the customer
        result = intramove_db["customers"].update_one(query, update)
        if result.acknowledged:
            print("Customer set to inactive.")
        return {"error": "recharge is required"}

    update = {"$inc": {"credits": -1}}
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
        "datetime": datetime,
        "sign": selectedDescriptor.sign,
        "indicator": selectedDescriptor.indicator,
        "description": selectedDescriptor.description,
        "score": score,
        "api_key": api_key,
    }

    "Ensure you're using production DB"
    intramove_db["headlines"].insert_one(
        output_dict,
    )

    del output_dict["_id"]
    del output_dict["api_key"]

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
