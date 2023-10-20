from flask import Flask, render_template
import requests
import plotly.express as px

app = Flask(__name__)

# Replace with your own NHS API key
API_KEY = ""

def get_nhs_data():
    url = "https://api.coronavirus.data.gov.uk/v1/data"
    params = {
        "filters": "areaType=nation;areaName=england",
        "structure": '{"date":"date","cases":"newCasesByPublishDate"}',
    }
    headers = {"X-Api-Key": API_KEY}

    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data

@app.route('/')
def display_data():
    data = get_nhs_data()

    # Extract dates and cases from the response
    dates = [entry['date'] for entry in data['data']]
    cases = [entry['cases'] for entry in data['data']]

    # Create a bar graph using Plotly
    fig = px.bar(x=dates, y=cases, labels={'x': 'Date', 'y': 'New Cases'})
    fig.update_layout(title='NHS COVID-19 Data for England')

    return render_template('graph.html', graph_json=fig.to_json())

if __name__ == '__main__':
    app.run(debug=True)
