from flask import Flask, jsonify

from src.dashboardScraper import DashboardScraper

# app variable (should be the same for each Flask app)
app = Flask(__name__)

scraper = DashboardScraper()
scraper.connect()

@app.route('/', methods=['GET'])
def get_data():
    scraper.refresh()
    data = scraper.get_json_data()
    return jsonify(data)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5001)