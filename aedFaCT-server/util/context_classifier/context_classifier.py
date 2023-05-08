import joblib

import os
dirname = os.path.dirname(__file__)
cs_filename = os.path.join(dirname, 'models/cs.joblib')
bio_filename = os.path.join(dirname, 'models/bio.joblib')
fin_filename = os.path.join(dirname, 'models/fin.joblib')

models = {}

models['cs'] = joblib.load(cs_filename)
models['bio'] = joblib.load(bio_filename)
models['fin'] = joblib.load(fin_filename)

def predict_tags(X):
    preds = []
    # convert into iterable if string
    if type(X) is str:
        X = [X]

    # get prediction from each model
    for c in models.keys():
        preds.append(models[c].predict(X))

    return [k for k,v in zip(list(models.keys()),preds) if v[0] > 0]
