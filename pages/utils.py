import pickle


def get_price_from_model(item_information):
    encoder = pickle.load(open('models/encoder.obj', 'rb'))
    model = pickle.load(open('models/model_dtr.pkl', 'rb'))

    encoded_data = encoder.transform(item_information)
    prediction = model.predict(encoded_data)
    return prediction
