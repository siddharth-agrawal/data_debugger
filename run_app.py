import sqlite3

from utils.input_utils import get_input
from utils import query_utils


class DataAPI:
    def __init__(self, mode):
        self.db_conn = sqlite3.connect("enriched_data.db")
        self.mode = mode

        # get data depending on mode
        if mode == 1:
            self.data = query_utils.get_possible_mistakes(self.db_conn)
        elif mode == 2:
            self.data = query_utils.get_labels_verify(self.db_conn)

        self.point = 0


    def is_remaining(self):
        # if there's data remaining to be shown
        return (self.point < len(self.data))


    def next_row(self):
        # message depending on mode
        if self.mode == 1:
            self.display_mistake_message()
        if self.mode == 2:
            self.display_verify_message()
        self.point += 1


    def display_verify_message(self):
        row = self.data[self.point:self.point+1]

        message_dict = {
            'text': row['text'].tolist()[0],
            'predicted_label': row['pred_label'].tolist()[0],
            'prediction_confidence': row['pred_confidence'].tolist()[0],
            'confusion_score': row['score'].tolist()[0]
        }
        value = get_input('Do you want to use the predicted label?',
            ['Yes', 'No'], message_dict)

        # exit app
        if value == 0:
            self.point = len(self.data)

        # update label
        if value == 1:
            query_utils.update_label(row['id'].tolist()[0],
                row['pred_label'].to_list()[0], self.db_conn)
            print('\n\nAnnotation updated!')


    def display_mistake_message(self):
        row = self.data[self.point:self.point+1]

        message_dict = {
            'text': row['text'].tolist()[0],
            'existing_label': row['intent'].tolist()[0],
            'predicted_label': row['pred_label'].tolist()[0],
            'prediction_confidence': row['pred_confidence'].tolist()[0]
        }
        value = get_input('Do you want to update the label?', ['Yes', 'No'],
            message_dict)

        # exit app
        if value == 0:
            self.point = len(self.data)
            return

        # update label
        if value == 1:
            query_utils.update_label(row['id'].tolist()[0],
                row['pred_label'].tolist()[0], self.db_conn)
            print('\n\nAnnotation updated!')


def run_app():
    # two modes that the app can run in, more info in README
    value = get_input('Which mode do you want to run the app in?',
        ['Correct potential mistakes', 'Verify predicted labels'])
    if value == 0:
        return
    
    api = DataAPI(value)
    while api.is_remaining():
        api.next_row()

    print('\n\nShutting down app...')


if __name__ == '__main__':
    run_app()
