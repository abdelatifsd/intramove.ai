from typing import List
import re, requests, os


def naive_chunker(text: str) -> List[str]:
    chunked_text = re.split("[|!?.,:;()[\\]]", text)
    chunked_text = [text.lstrip().rstrip() for text in chunked_text]
    chunked_text = [text for text in chunked_text if text]
    return chunked_text


def chunker_api(input_text: str) -> List[str]:
    # Call chunker API
    url = os.getenv("CHUNKER_API")
    lang = "en"
    params = {"text": input_text, "lang": lang}
    response = requests.post(url, params).json()["results"]
    return [sentence["chunk"] for sentence in response[::-1]]
