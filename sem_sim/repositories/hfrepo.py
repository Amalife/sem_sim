from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer
from sem_sim.configuration.configuration import configuration

# Интерфейс эмбеддеров из Hugging Face
class HFRepo:
    def __init__(self):
        self.model = SentenceTransformer(configuration.project_root / "models" / configuration.model_name)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        embeds = np.array()
        for text in texts:
            if configuration.model_name in ["frida", "berta"]:
                np.append(embeds, self.model.encode(text, prompt_name="search_query"))
            else:
                np.append(embeds, self.model.encode(text))
