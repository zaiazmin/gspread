import json
import os
from app import app
from models import db, User, ToolHolder, Insert

def init_db():
    # Path to sample data
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = os.path.join(BASE_DIR, '..', 'design_specs', 'sample_data.json')

    # Load JSON
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    with app.app_context():
        # Create Tables
        db.create_all()
        print("Tables created.")

        # Seed Users
        if not User.query.first():
            print("Seeding Users...")
            for u in data['users']:
                user = User(
                    user_id=u['user_id'],
                    username=u['username'],
                    role=u['role'],
                    full_name=u['full_name'],
                    department=u['department']
                )
                db.session.add(user)

        # Seed Tool Holders
        if not ToolHolder.query.first():
            print("Seeding Tools...")
            for t in data['tool_holders']:
                tool = ToolHolder(
                    id=t['id'],
                    iso_code=t['iso_code'],
                    category=t['category'],
                    description=t['description'],
                    location=t['location'],
                    stock=t['stock'],
                    compatible_inserts_json=json.dumps(t['compatible_inserts'])
                )
                db.session.add(tool)

        # Seed Inserts
        if not Insert.query.first():
            print("Seeding Inserts...")
            for i in data['inserts']:
                insert = Insert(
                    id=i['id'],
                    iso_code=i['iso_code'],
                    grade=i['grade'],
                    material_app=i['material_app'],
                    coating=i['coating'],
                    manufacturer=i['manufacturer'],
                    stock_quantity=i['stock_quantity'],
                    min_alert_level=i['min_alert_level'],
                    box_quantity=i['box_quantity']
                )
                db.session.add(insert)

        db.session.commit()
        print("Database seeded successfully.")

if __name__ == '__main__':
    init_db()
