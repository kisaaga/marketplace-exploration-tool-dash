import pickle


def get_price_from_model(item_information):
    encoder = pickle.load(open('models/encoder.obj', 'rb'))
    model = pickle.load(open('models/model_dtr.pkl', 'rb'))

    encoded_data = encoder.transform(item_information)
    prediction = model.predict(encoded_data)
    return prediction


def get_sales_from_model(dataset, k, week_or_month):
    ar_model = pickle.load(open('models/Ar_model.pickle', 'rb'))

    future_pred_month = ar_model.predict(start=len(dataset), end=(len(dataset) + 30 * k), dynamic=False)
    future_pred_week = ar_model.predict(start=len(dataset), end=(len(dataset) + 7 * k), dynamic=False)
    wdaily = []
    mdaily = []
    wpsales = 0
    mpsales = 0
    for i in range(7):
        wpsales = wpsales + future_pred_week[i]
        wdaily.append(int(future_pred_week[i]))
    for i in range(30 * k):
        mpsales = mpsales + future_pred_month[i]
        mdaily.append(int(future_pred_month[i]))

    if week_or_month == 'Week':
        return wpsales, wdaily

    elif week_or_month == 'Month':
        return mpsales, mdaily
