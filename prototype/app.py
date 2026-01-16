from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# Load data relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, '..', 'design_specs', 'sample_data.json')

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/data')
def get_data():
    data = load_data()

    # Calculate some summary metrics for the dashboard
    total_tools = sum(t['stock'] for t in data.get('tool_holders', []))
    total_inserts = sum(i['stock_quantity'] for i in data.get('inserts', []))

    low_stock_inserts = [
        i for i in data.get('inserts', [])
        if i['stock_quantity'] <= i['min_alert_level']
    ]

    active_loans = 3 # Hardcoded mock from "Active Loans" design spec

    summary = {
        'total_tools': total_tools,
        'total_inserts': total_inserts,
        'low_stock_count': len(low_stock_inserts),
        'active_loans': active_loans,
        'low_stock_items': low_stock_inserts
    }

    return jsonify({
        'raw_data': data,
        'summary': summary
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
