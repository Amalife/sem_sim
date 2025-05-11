import numpy as np
from nltk.util import ngrams

from sem_sim.configuration.configuration import configuration
from sem_sim.logger.logger import app_logger

def make_ids(sent):
    word_indices = []
    length = len(sent)
    i = 0

    while i < length:
        if sent[i].isspace():
            i += 1
            continue

        start = i
        while i < length and not sent[i].isspace():
            i += 1
        end = i - 1

        word_indices.append((start, end+1))

    return word_indices

def make_ngrams_ids(sent_ids):
    a = [tuple(sent_ids[i:i+2]) for i in range(len(sent_ids) - 1)]
    bigram_ids = [tuple([val[0][0], val[-1][-1]]) for val in a]

    a = [tuple(sent_ids[i:i+3]) for i in range(len(sent_ids) - 2)]
    trigram_ids = [tuple([val[0][0], val[-1][-1]]) for val in a]
    return bigram_ids, trigram_ids

def make_ngrams(sent):
    sent_unogram = sent.split()
    bigram = ngrams(sent_unogram, 2)
    trigram = ngrams(sent_unogram, 3)
    sent_bigram = [" ".join(words) for words in bigram]
    sent_trigram = [" ".join(words) for words in trigram]

    return sent_unogram, sent_bigram, sent_trigram

def find_words_scores(embeds_ids, phrase_embed, sent):
    all_sims = []
    for (embed_list, words_ids) in embeds_ids:
        sims = []
        for embed in embed_list:
            sims.append(np.dot(embed.embedding / np.linalg.norm(embed.embedding), phrase_embed.embedding / np.linalg.norm(phrase_embed.embedding)))
        all_sims.append((sims, words_ids))
    app_logger.info("Got similarity table: %s", all_sims)
    ngram_max_id = np.argmax([np.max(k) for k in [v[0] for v in all_sims]])
    cur_sims = all_sims[ngram_max_id]
    sort_sims = sorted(list(zip(cur_sims[0], cur_sims[1])), reverse=True)
    top1 = sort_sims[0]
    results = [top1]
    for val in sort_sims[1:]:
        if abs(val[0] - top1[0]) < configuration.sim_epsilon:
            results.append(val)
        else:
            break
    words = []
    for res in results:
        words.append(sent[res[1][0]:res[1][1]])
    return results, words


def check_sent_sim(sent_embed, phrase_embed):
    score = np.dot(sent_embed.embedding / np.linalg.norm(sent_embed.embedding), phrase_embed.embedding / np.linalg.norm(phrase_embed.embedding))
    app_logger.info("Got sent scores %s", score)
    if score >= configuration.sent_thresh:
        return True
    else:
        return False