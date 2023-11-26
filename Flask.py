from flask import Flask,render_template, jsonify, request
import pandas as pd
from prophet import Prophet

app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# Load the dataset into a pandas DataFrame
data = pd.read_csv('monatszahlen2307_verkehrsunfaelle_10_07_23_nosum.csv')

# Data processing steps
data_until_2020 = data[data['JAHR'] <= 2020].copy()
data_until_2020 = data_until_2020.dropna()
data_until_2020['MONAT'] = data_until_2020['MONAT'].astype(str).str[-2:].astype(int)

@app.route('/')
def index():
    # Specific options for Category and Type
    categories = ['Alkoholunfälle', 'Verkehrsunfälle', 'Fluchtunfälle']  
    types = ['insgesamt', 'Verletzte und Getötete', 'mit Personenschäden']  

    return render_template('index.html', categories=categories, types=types)

@app.route('/forecast', methods=['POST'])
def get_forecast():
    req_data = request.get_json()
    category = req_data.get('category', 'Alkoholunfälle')
    _type = req_data.get('type', 'insgesamt')
    year = int(req_data.get('year', 2021))
    month = int(req_data.get('month', 1))

    category_data = data_until_2020[
        (data_until_2020['MONATSZAHL'] == category) &
        (data_until_2020['AUSPRAEGUNG'] == _type)
    ]
    
    prophet_data = category_data[['JAHR', 'MONAT', 'WERT']]
    prophet_data.columns = ['ds', 'month', 'y']
    prophet_data['ds'] = pd.to_datetime(prophet_data['ds'].astype(str) + prophet_data['month'].astype(str).str.zfill(2), format='%Y%m')

    model = Prophet()
    model.fit(prophet_data)

    future = model.make_future_dataframe(periods=12, freq='M')
    forecast = model.predict(future)

    specific_prediction = forecast[(forecast['ds'].dt.year == year) & (forecast['ds'].dt.month == month)][['ds', 'yhat']]
    predicted_value = specific_prediction['yhat'].values[0]

    return jsonify({'category': category, 'type': _type, 'year': year, 'month': month, 'predicted_value': predicted_value})

if __name__ == '__main__':
    app.run(debug=True)
