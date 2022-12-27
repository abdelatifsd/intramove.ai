from typing import List
import re, requests, os
import nltk

nltk.download("punkt")


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


def advanced_chunker(text):
    # Break sentences down
    sentences = nltk.sent_tokenize(text)

    tokenized_sentences = []
    # Split tokenized sentences based on full-stop punct (without splitting digits)
    for sentence in sentences:
        split_sentences = re.split(r",(?!\d)", sentence)
        tokenized_sentences.extend(split_sentences)

    # Retokenize after previous split
    final_tokenization = []
    for tokenized_sentence in tokenized_sentences:
        retokenized_sentences = nltk.sent_tokenize(tokenized_sentence)
        final_tokenization.extend(retokenized_sentences)

    final_tokenization = [
        tokenized_sentence.strip() for tokenized_sentence in final_tokenization
    ]
    return final_tokenization
