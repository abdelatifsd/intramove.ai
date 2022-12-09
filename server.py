from service import FinancialIndex
from utils.chunker import chunker_api

import datetime, requests, os, argparse, subprocess, logging, json
from typing import BinaryIO, Union

from sentence_transformers import SentenceTransformer
import pandas as pd

import uvicorn
from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import StreamingResponse, JSONResponse

from pymongo import MongoClient
import bson

from dotenv import load_dotenv

logging.getLogger().setLevel(logging.INFO)
load_dotenv() 

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

### END POINTS ###
@app.get("/")
def home():
    return JSONResponse({"text":"welcome to intramove.ai"})


@app.post("/analyze")
def analyze(headline: str = Query(), 
            article: str = Query(),
            datetime: str = Query(),
            callback_url: str = Query()):
    pass

@app.post("/analyze/headline")
def analyzeHeadline(headline: str = Query(), 
                    datetime: str = Query(),
                    callback_url: str = Query()):
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
    
  
    intramove_db["headline"].insert_one(output_dict,)

    del output_dict["_id"]

    if not callback_url:
        return JSONResponse(output_dict)
    else:
        requests.post(
            callback_url,
            json=output_dict,
        )

@app.post("/analyze/article")
def analyzeArticle(article: str = Query(), 
                    datetime: str = Query(),
                    callback_url: str = Query()):

    chunked_text = chunker_api(article)
    chunks_analysis = [] # text:results
    average_score  = 0

    for chunk in chunked_text:
        document_embedding = initializedFinaIndex.encodeText(
            chunk
        )
        scores, indices = initializedFinaIndex.index.search(document_embedding, 1)
        scores = scores.flatten()
        indices = indices.flatten()
        if scores[0] > 0.6:
            selectedDescriptor = initializedFinaIndex.final_descriptors[indices[0]]
            if selectedDescriptor.sign == "bull":
                average_score+=scores[0]
                score = float(scores[0])
            elif selectedDescriptor.sign == "bear":
                average_score-=scores[0]
                score = float(scores[0])*-1

            chunk_analysis = {"chunk":chunk,
                            "sign":selectedDescriptor.sign,
                            "indicator":selectedDescriptor.indicator,
                            "description":selectedDescriptor.description,
                            "score":score}

            chunks_analysis.append(chunk_analysis)


    output_dict = {"chunks":chunks_analysis,
                "average_score":average_score,
                "average_sign":"bull" if average_score > 0 else "bear",
                "datetime":datetime}

    intramove_db["article"].insert_one(output_dict,)

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
