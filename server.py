from service import FinancialIndex
from utils.chunker import chunker_api
import os, subprocess

from sentence_transformers import SentenceTransformer
import datetime, urllib.request, requests, os, argparse
from typing import BinaryIO, Union

import uvicorn
from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import StreamingResponse, JSONResponse


app = FastAPI()

@app.get("/")
def home():
    return JSONResponse({"text":"welcome to intramove.ai"})


@app.post("/analyze")
def analyze(headline: str = Query(), article: str = Query()):
    pass

@app.post("/analyze/headline")
def analyzeHeadline(headline: str = Query(), callback_url: str = Query()):
    document_embedding = initializedFinaIndex.encodeText(
        headline
    )
    scores, indices = initializedFinaIndex.index.search(document_embedding, 1)
    scores = scores.flatten()
    indices = indices.flatten()

    selectedDescriptor = initializedFinaIndex.final_descriptors[indices[0]]

    output_dict = {"text":headline,
                "sign":selectedDescriptor.sign,
                "indicator":selectedDescriptor.indicator,
                "description":selectedDescriptor.description,
                "score":str(scores[0])}

    if not callback_url:
        return JSONResponse(output_dict)
    else:
        requests.post(
            callback_url,
            json=output_dict,
        )

@app.post("/analyze/article")
def analyzeHeadline(article: str = Query(), callback_url: str = Query()):

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
        if scores[0] > 0.4:
            selectedDescriptor = initializedFinaIndex.final_descriptors[indices[0]]
            if selectedDescriptor.sign == "bull":
                average_score+=scores[0]
            elif selectedDescriptor.sign == "bear":
                average_score-=scores[0]

            chunk_analysis = {"chunk":chunk,
                            "sign":selectedDescriptor.sign,
                            "indicator":selectedDescriptor.indicator,
                            "description":selectedDescriptor.description,
                            "score":str(scores[0])}

            chunks_analysis.append(chunk_analysis)


    output_dict = {"chunks":chunks_analysis,
                "average_score":average_score,
                "average_sign":"bull" if average_score > 0 else "bear"}

    if not callback_url:
        return JSONResponse(output_dict)
    else:
        requests.post(
            callback_url,
            json=output_dict,
        )


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
