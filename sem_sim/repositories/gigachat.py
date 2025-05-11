from typing import List

from gigachat import GigaChat
from sem_sim.configuration.configuration import configuration

# Интерфейс гигачат эмбеддера
class GigaChatRepo:
    def __init__(self):
        self.client = GigaChat(
            credentials=configuration.gigachat_credentials,
            scope=configuration.gigachat_scope,
            verify_ssl_certs=False,
        )

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return self.client.embeddings(texts).data
