import faiss
import numpy as np
from utils import inverse_indicators, phrases, selected_indicators
from sentence_transformers import SentenceTransformer
import pickle

class FinancialDescriptor:
    def __init__(self, description, embedding, sign):
        self.description = description
        self.embedding = embedding
        self.sign = sign
        self.score = None

class FinancialIndex:
    def __init__(self, device: str, load: bool):
        self.model = SentenceTransformer("sentence_models/all-mpnet-base-v2")
        self.device = device
        self.final_descriptors = None
        self.index = self.generateFinancialIndex(load=load)

    def encodeText(self, text: str):
        return self.model.encode([text], device=self.device)

    def generateDescriptions(self) -> tuple:
        bullish_descriptions = []
        bearish_descriptions = []

        inverse_relation_indicators = [
            invr_indicator.lower()
            for invr_indicator in inverse_indicators.inverse_relation_indicators
        ]

        indicators = selected_indicators.indicators.split(
            ","
        )  # [index].replace("\n","")
        indicators = [indicator.replace("\n", "").lower() for indicator in indicators]
        indicators = list(set(indicators))

        for i, indicator in enumerate(indicators):
            if indicator not in inverse_relation_indicators:
                for bull_phrase in phrases.bullish_phrases:
                    bullish_descriptions.append(f"{indicator} {bull_phrase}")

                for bear_phrase in phrases.bearish_phrases:
                    bearish_descriptions.append(f"{indicator} {bear_phrase}")

            else:
                for bull_phrase in phrases.bullish_phrases:
                    bearish_descriptions.append(f"{indicator} {bull_phrase}")

                for bear_phrase in phrases.bearish_phrases:
                    bullish_descriptions.append(f"{indicator} {bear_phrase}")

        return bullish_descriptions, bearish_descriptions

    def generateFinancialDescriptors(self):
        bullish_descriptors = []
        bearish_descriptors = []

        bullish_descriptions, bearish_descriptions = self.generateDescriptions()

        for description in bullish_descriptions:
            description_embedding = self.encodeText(description)

            fblob = FinancialDescriptor(
                description=description, embedding=description_embedding, sign="bull"
            )
            bullish_descriptors.append(fblob)

        for description in bearish_descriptions:
            description_embedding = self.encodeText(description)
            fblob = FinancialDescriptor(
                description=description, embedding=description_embedding, sign="bear"
            )
            bearish_descriptors.append(fblob)
        return bullish_descriptors, bearish_descriptors

    def generateFinancialIndex(self, load:bool=False):
        if not load:
            bullish_descriptors, bearish_descriptors = self.generateFinancialDescriptors()
            self.final_descriptors = bullish_descriptors + bearish_descriptors
            with open('data/final_descriptors.pickle', 'wb') as pkl:
                pickle.dump(self.final_descriptors, pkl)
            final_embeddings = [blob.embedding.squeeze() for blob in self.final_descriptors]
            final_embeddings = np.array(final_embeddings)
            index = faiss.IndexFlatIP(final_embeddings.shape[1])
            faiss.normalize_L2(final_embeddings)
            index.add(final_embeddings)
        else:
            with open('data/final_descriptors.pickle', 'rb') as pkl:
                self.final_descriptors = pickle.load(pkl)
            final_embeddings = [blob.embedding.squeeze() for blob in self.final_descriptors]
            final_embeddings = np.array(final_embeddings)
            index = faiss.IndexFlatIP(final_embeddings.shape[1])
            faiss.normalize_L2(final_embeddings)
            index.add(final_embeddings)

        return index
