from service import FinancialIndex
from utils.chunker import advanced_chunker

import requests, os, argparse, subprocess, logging, json
from typing import BinaryIO, Union
from datetime import datetime

from sentence_transformers import SentenceTransformer
import pandas as pd
import faiss

import uvicorn
from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import StreamingResponse, JSONResponse

from pymongo import MongoClient
import bson

from dotenv import load_dotenv

logging.getLogger().setLevel(logging.INFO)
load_dotenv(".envlocal")


def initMongo():

    uri = os.getenv("MONGO_DB_URI")
    cert_path = os.path.expanduser(os.getenv("MONGO_DB_CERT_PATH"))
    client = MongoClient(uri, tls=True, tlsCertificateKeyFile=cert_path)
    db = client["NewsAnalysis"]
    return db


app = FastAPI()

intramove_db = initMongo()

### END POINTS ###
@app.get("/")
def home():
    return JSONResponse({"text": "welcome to intramove.ai"})


@app.post("/analyze")
def analyze(
    headline: str = Query(),
    article: str = Query(),
    datetime: str = Query(),
    callback_url: str = Query(),
):
    pass


@app.post("/analyze/headline")
def analyzeHeadline(
    headline: str = Query(), date_time: str = Query(), callback_url: str = Query()
):
    document_embedding = initializedFinaIndex.encodeText(headline)
    scores, indices = initializedFinaIndex.index.search(document_embedding, 1)
    scores = scores.flatten()
    indices = indices.flatten()

    selectedDescriptor = initializedFinaIndex.final_descriptors[indices[0]]

    if selectedDescriptor.sign == "bull":
        score = float(scores[0])
    elif selectedDescriptor.sign == "bear":
        score = float(scores[0]) * -1

    # process dates

    """date_time = datetime.strptime(date_time, "%m/%d/%Y")
    date_time = date_time.isoformat()
    date_time = datetime.fromisoformat(date_time)"""

    output_dict = {
        "text": headline,
        "datetime": date_time,
        "sign": selectedDescriptor.sign,
        "indicator": selectedDescriptor.indicator,
        "description": selectedDescriptor.description,
        "score": score,
    }

    intramove_db["headline"].insert_one(
        output_dict,
    )

    del output_dict["_id"]

    if not callback_url:
        return JSONResponse(output_dict)
    else:
        requests.post(
            callback_url,
            json=output_dict,
        )


@app.post("/analyze/article")
def analyzeArticle(
    article: str = Query(), date_time: str = Query(), callback_url: str = Query()
):

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
            score = float(max_scores[descriptor_index]) * -1

        if score > 0.5:
            chunk_analysis = {
                "chunk": chunks[descriptor_index],
                "sign": selectedDescriptor.sign,
                "indicator": selectedDescriptor.indicator,
                "description": selectedDescriptor.description,
                "score": score,
            }

            chunks_analysis.append(chunk_analysis)

    # process dates

    """date_time = datetime.strptime(date_time, "%m/%d/%Y")
    date_time = date_time.isoformat()
    date_time = datetime.fromisoformat(date_time)"""

    output_dict = {
        "chunks": chunks_analysis,
        "average_score": average_score,
        "average_sign": "bull" if average_score > 0 else "bear",
        "datetime": date_time,
    }

    intramove_db["article"].insert_one(
        output_dict,
    )

    del output_dict["_id"]

    if not callback_url:
        return JSONResponse(output_dict)
    else:
        requests.post(
            callback_url,
            json=output_dict,
        )

@app.post("/database/update/date")
def updateDates():
    intramove_db["headline"].update_many(
        {}, [{"$set": {"datetime": {"$toDate": "$datetime"}}}]
    )

    
@app.post("/database/update/timezone")
def updateTimezone():
    import pytz
    # Get the GMT and EST time zones
    gmt_tz = pytz.timezone('GMT')
    est_tz = pytz.timezone('EST')

    # Find the documents with dates in GMT
    query = {'datetime': {'$exists': True}}
    projection = {'_id': 1, 'datetime': 1}
    article_gmt_documents = intramove_db["article"].find(query, projection)
    headline_gmt_documents = intramove_db["headline"].find(query, projection)

    # Convert the dates to EST and update the documents
    for doc in article_gmt_documents:
        gmt_date = doc['datetime']
        est_date = gmt_date.astimezone(est_tz)

        update_query = {'_id': doc['_id']}
        update_operator = {'$set': {'datetime': est_date}}
        intramove_db["article"].update_one(update_query, update_operator)
    
    # Convert the dates to EST and update the documents
    for doc in headline_gmt_documents:
        gmt_date = doc['datetime']
        est_date = gmt_date.astimezone(est_tz)

        update_query = {'_id': doc['_id']}
        update_operator = {'$set': {'datetime': est_date}}
        intramove_db["headline"].update_one(update_query, update_operator)


@app.post("/database/delete")
def deleteRecordsDates(iso_date: str = Query()):

    query = {'datetime':iso_date}

    # Delete the documents
    r = intramove_db["headline"].delete_many(query)
    intramove_db["article"].delete_many(query)
    
    print(r.deleted_count)

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
