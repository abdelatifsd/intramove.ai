from sentence_transformers import SentenceTransformer
import argparse, os

def download_sentence_model(modelName:str):
    modelPath = "sentence_models/"
    model = SentenceTransformer(modelName)
    model.save(modelPath+"/"+modelName)


if __name__ == "__main__":
    """parser = argparse.ArgumentParser()
    parser.add_argument(
        "-sm",
        "--sentence_model_name",
        dest="sentence_model_name",
        type=str,
        required=False,
        help="sentence transformer model name to download",
    )
    args = parser.parse_args()"""
    os.mkdir("sentence_models")
    #download_sentence_model("paraphrase-multilingual-MiniLM-L12-v2")
    download_sentence_model(os.getenv("SENTENCE_TRANSFORMER_MODEL"))
