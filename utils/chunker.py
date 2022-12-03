from typing import List
import re, requests

def naive_chunker(text:str)->List[str]:
  chunked_text = re.split('[|!?.,:;()[\\]]', text)
  chunked_text = [text.lstrip().rstrip() for text in chunked_text]
  chunked_text = [text for text in chunked_text if text]
  return chunked_text


def chunker_api(input_text:str)->List[str]:
  # Call chunker API
  url = "https://api.repustate.com/v4/12856c614b13af33f55ffb8ac5b3838f724d21da57d024970481973f/chunk.json"
  lang = "en"
  params = {"text":input_text,"lang":lang}
  response = requests.post(url, params).json()["results"]
  return [sentence["chunk"] for sentence in response[::-1]]