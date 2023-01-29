from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__, template_folder='web')


@app.route('/')
def student():
    return render_template("home.html")


def ValuePredictor(to_predict_list, to_option):
    to_predict = [to_predict_list]
    if to_option=='Regression1':
        loaded_model = joblib.load('/Users/coding/Documents/vs/machine_learning/ml_algos/model.sav')                                           
        result = loaded_model.predict(to_predict)
    if to_option=='Regression2':
        loaded_model = joblib.load('/Users/coding/Documents/vs/machine_learning/ml_algos/model2.sav')                                           
        result = loaded_model.predict(to_predict)
    if to_option=='Classifier1':
        loaded_model = joblib.load('/Users/coding/Documents/vs/machine_learning/ml_algos/model3.sav')                                             
        result = loaded_model.predict(to_predict)
    if to_option=='Classifier2':
        loaded_model = joblib.load('/Users/coding/Documents/vs/machine_learning/ml_algos/model4.sav')                                             
        result = loaded_model.predict(to_predict)
    if to_option=='Classifier3':
        loaded_model = joblib.load('/Users/coding/Documents/vs/machine_learning/ml_algos/model5.sav')                                             
        result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        #to_option = request.form.getlist('model')
        #to_predict_list = request.form.getlist("feature1")
        #to_predict_list = list(map(float,int(to_predict_list)))
        tol = request.form
        tol2 = tol.to_dict()
        tol3 = tol2.pop('model')
        tol2 = tol2.values()
        to_predict_list = list(tol2)
        to_predict_list = [int(i) for i in to_predict_list]
        res = ValuePredictor(to_predict_list, tol3)
        if res== 1:
            result='YES'
        else:
            result='NO'
        return render_template("home.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)