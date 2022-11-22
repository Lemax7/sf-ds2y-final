import os
import sys

import numpy as np
import pickle


if 'lightfm_model.pickle' not in os.listdir():
    print(os.listdir())
    if 'lightfm_model.tar.xz.part_aa' in os.listdir():
        os.system('cat lightfm_model.tar.xz.part_* > lightfm_model.tar.xz && tar -xf lightfm_model.tar.xz')
    else:
        print('No LightFM model archive in current directory')
        sys.exit(1)

with open('lightfm_model.pickle', 'rb') as f:
    model = pickle.load(f)

with open('lightfm_data_mapping.pickle', 'rb') as f:
    dataset_mapping = pickle.load(f)
    
visitorid_mapping, _, itemid_mapping, _ = dataset_mapping
visitorid_labels = {v:k for k, v in visitorid_mapping.items()}
itemid_labels = {v:k for k, v in itemid_mapping.items()}


def get_inner_model_visitorid(visitorid):
    return visitorid_mapping.get(visitorid)


def get_inner_model_itemid(itemid):
    return itemid_mapping.get(itemid)


def get_original_visitorid(inner_visitorid):
    return visitorid_labels.get(inner_visitorid)


def get_original_itemid(inner_itemid):
    return itemid_labels.get(inner_itemid)


def generate_top5_recommendations():
    pass


def predict(visitorid):
    inner_model_visitorid = get_inner_model_visitorid(visitorid)
    if not inner_model_visitorid:
        return []
    pred_scores = model.predict(inner_model_visitorid, np.arange(len(itemid_mapping)))
    top_scores = np.argsort(-pred_scores)[:3]
    return [itemid_labels[k] for k in top_scores]


def check_visitor(visitorid):
    return visitorid_mapping.get(visitorid, False) != False