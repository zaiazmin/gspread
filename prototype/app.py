from flask import Flask, render_template, jsonify
import json
import os
from models import db, User, ToolHolder, Insert

app = Flask(__name__)

# Configure SQLite Database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'inventory.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/data')
def get_data():
    # Fetch data from Database
    tools = ToolHolder.query.all()
    inserts = Insert.query.all()
    users = User.query.all()

    # Calculate summary metrics
    total_tools = sum(t.stock for t in tools)
    total_inserts = sum(i.stock_quantity for i in inserts)

    low_stock_inserts = [
        i for i in inserts
        if i.stock_quantity <= i.min_alert_level
    ]

    active_loans = 3 # Still mocked until Loan table logic is added

    summary = {
        'total_tools': total_tools,
        'total_inserts': total_inserts,
        'low_stock_count': len(low_stock_inserts),
        'active_loans': active_loans,
        'low_stock_items': [{
            'iso_code': i.iso_code,
            'manufacturer': i.manufacturer,
            'stock_quantity': i.stock_quantity,
            'min_alert_level': i.min_alert_level
        } for i in low_stock_inserts]
    }

    # Serialize for JSON response
    raw_data = {
        'tool_holders': [{
            'iso_code': t.iso_code,
            'category': t.category,
            'description': t.description,
            'location': t.location,
            'stock': t.stock
        } for t in tools],
        'inserts': [], # Not needed for dashboard table currently
        'users': [{'username': u.username, 'role': u.role} for u in users]
    }

    return jsonify({
        'raw_data': raw_data,
        'summary': summary
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Auto-create DB if not exists (for convenience)
    if not os.path.exists(DB_PATH):
        print("Database not found. Initializing...")
        import init_db
        init_db.init_db()

    app.run(host='0.0.0.0', port=port, debug=True)
