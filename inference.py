import numpy as np
import sys
import os
import time
import json
import jieba
import NLP_training
from NLP_training import transform_to_conll_format
import torch
import pickle
from torch.autograd import Variable
from pathlib import Path
import logging

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

def main(input_path, result_path):
    model = NLP_training.LSTMParser()
    model.load_state_dict(torch.load("lang_{}/models/{}.pth".format("zh", "model1_e29")))
    for file in Path(input_path).glob('**/*.txt'):
        logging.info("file{}".format(file))
        mid = os.path.relpath(str(file), input_path)
        logging.info("mid{}".format(mid))
        dst_json = os.path.join(result_path, os.path.dirname(mid), str(file.stem) + '.json')
        logging.info("dst_json{}".format(dst_json))
        os.makedirs(os.path.dirname(dst_json), exist_ok=True)

        data_list = []
        word_tokens = []
        with open(str(file), 'r') as f:
            for line in f:
                tokens = [word for word in jieba.cut(line.strip())]
                word_tokens.append(tokens)
                for idx, token in enumerate(tokens):
                    sample = []
                    sample.append(idx + 1)
                    sample.append(idx + 1)
                    sample.append(token)
                    sample.append("_")
                    sample.append("_")
                    sample.append("_")
                    data_list.append(sample)
        sentences = transform_to_conll_format(data_list)
        with open('lang_{}/embeddings/i2label.pickle'.format("zh"), 'rb') as file:
            i2label = pickle.load(file)
        test_start_time = time.time()
        json_obj = []
        for i in range(len(sentences)):
            sentence = sentences[i]
            sentence_var = Variable(NLP_training.embed_sentence(sentence, "zh"), requires_grad=False)
            arc_prediction, label_prediction = model.predict(sentence_var)
            sentence_json_obj = {}
            sentence_json_obj["ID"] = i
            sentence_json_obj["text"] = "".join(word_tokens[i])
            sentence_json_obj["words"] = []
            for id, token in enumerate(sentence):
                if id == len(word_tokens[i]):
                    break
                token_obj = {}
                token_obj["id"] = id + 1
                token_obj["form"] = word_tokens[i][id]
                token_obj["head"] = np.argmax(arc_prediction[id])
                token_obj["pos"] = ""
                token_obj["deprel"] = ""
                token_obj["stanfordnlpdependencies"] = ""
                sentence_json_obj["words"].append(token_obj)
            json_obj.append(sentence_json_obj)
        test_time = time.time() - test_start_time
        with open(dst_json, 'w', encoding='utf-8') as f:
            json.dump(json_obj, f, indent=4, ensure_ascii=False, cls=NpEncoder)
        return len(sentences), test_time, json_obj