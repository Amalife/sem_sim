from typing import Tuple

from sem_sim.configuration.configuration import configuration
from sem_sim.logger.logger import app_logger
from sem_sim.repositories.gigachat import GigaChatRepo
#from sem_sim.repositories.hfrepo import HFRepo
from sem_sim.use_cases.utils import make_ids, make_ngrams, find_words_scores, check_sent_sim, make_ngrams_ids

# Класс логики сервиса
class SentProcessor:
    def __init__(self):
        if configuration.model_name == "gigachat":
            self.model_repo = GigaChatRepo()
        #elif configuration.model_name in ["frida", "berta", "e5_large", "sbert_synonymy"]:
            #self.model_repo = HFRepo()
        else:
            raise ValueError(f"Unknown model {configuration.model_name}")
    
    def find_word(self, sent: str, phrase: str) -> Tuple[str, float, str]:
        app_logger.info("got sent: %s phrase: %s", sent, phrase)
        # Перевод фразы в эмбеддинг
        phrase_embed = self.model_repo.embed_texts([phrase])
        # Перевод предложения в эмбеддинг
        sent_embed = self.model_repo.embed_texts([sent])
        # Проверка, что фраза близка к предложению
        if not check_sent_sim(sent_embed[0], phrase_embed[0]):
            app_logger.info("Not found similar words in sent")
            return None
        
        # Получениеи индексов слов в предложении
        word_sent_ids = make_ids(sent)
        # Получение индексов биграм и триграм в предложениях
        bigram_ids, trigram_ids = make_ngrams_ids(word_sent_ids)
        # Создание нграм
        unogram, bigram, trigram = make_ngrams(sent)

        # Перевод нграм в эмбеддинги
        unogram_embeds = self.model_repo.embed_texts(unogram)
        bigram_embeds = self.model_repo.embed_texts(bigram)
        trigram_embeds = self.model_repo.embed_texts(trigram)

        # Поиск ближайшей нграмы, близости и позиции
        return find_words_scores([(unogram_embeds, word_sent_ids), (bigram_embeds, bigram_ids), (trigram_embeds, trigram_ids)], 
                                 phrase_embed[0], sent)