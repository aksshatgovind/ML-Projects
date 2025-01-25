import requests
import json

def load_current_quiz_data():
    '''
    Loads all the details of the quiz the user gave at current
    '''
    url = "https://www.jsonkeeper.com/b/LLQT"
    response = requests.get(url)
    data = response.json()
    return data

def load_historical_quiz_data():
    '''
    Loads all the  previous quizzes given and details related to it
    '''
    url1 = "https://api.jsonserve.com/rJvd7g"
    url2 = "https://api.jsonserve.com/XgAgFJ"
    #response = requests.get(url1)                   # Example API
    response = requests.get(url2) 
    data = response.json()
    return data

if __name__ == '__main__':
    quizD = load_current_quiz_data()
    hisquizD = load_historical_quiz_data()

    folder_path_1 = 'Quiz Analyst/data/quiz_data.json'
    folder_path_2 = 'Quiz Analyst/data/hist_quiz_data.json'

    with open(folder_path_1, 'w') as json_file:
        json.dump(quizD, json_file, indent=4)

    with open(folder_path_2, 'w') as json_file:
        json.dump(hisquizD, json_file, indent=4)
