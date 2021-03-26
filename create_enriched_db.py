import json
import math
import pandas as pd
import requests

from ast import literal_eval
from sqlalchemy import create_engine


def make_request(text_list):
    payload = {
        "data": [{"text": text} for text in text_list],
        "n_best": 1
    }
    headers = {
        "X-API-Key": "fe20f8db14ca9cec47e9b1c9d982da9f",
        "Content-Type": "application/json"
    }
    url = "https://api.humanloop.com/projects/411/predict"

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    return json.loads(r.content)


def get_batch_response(batch_text):
    resp_json = make_request(batch_text)
    batch_resp = []

    for example in resp_json:
        # some responses don't have these values
        try:
            label = example['predictions'][0]['value'][0]['label']
        except:
            label = None

        try:
            confidence = example['predictions'][0]['value'][0]['confidence']
        except:
            confidence = None

        batch_resp.append({
            'pred_label': label,
            'pred_confidence': confidence
        })

    return batch_resp


def get_enriched_data(data, batch_size=20):
    num_batches = math.ceil(len(data) / batch_size)
    preds = []

    # iterate because of the recommended request size
    for batch_idx in range(num_batches):
        print(f'On batch {batch_idx+1} of {num_batches}')

        start = batch_idx* batch_size
        end = (batch_idx+1)*batch_size
        batch_text = data['text'][start:end].tolist()

        batch_resp = get_batch_response(batch_text)
        preds += batch_resp

    enriched_data = pd.concat([data, pd.DataFrame(preds)], axis=1)
    return enriched_data


def get_json_data():
    with open('chatbot_intent_classifier_data.json', 'r') as json_file:
        orig_data = json.load(json_file)
    data = pd.DataFrame(orig_data)

    # split text and intent into separate columns
    data = pd.concat([data, pd.DataFrame(
        data["data"].apply(literal_eval).to_list())], axis=1).drop("data",
            axis=1)

    return data


def create_enriched_db():
    data = get_json_data()
    enriched_data = get_enriched_data(data)

    # store as sqlite db
    engine = create_engine('sqlite:///enriched_data.db', echo=True)
    sqlite_connection = engine.connect()
    enriched_data.to_sql("enriched_data", sqlite_connection, index=False)


if __name__ == '__main__':
    create_enriched_db()
