import pytest
import sys
import os
import json

# Ensure we can import from the parent directory (prototype/)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, User, ToolHolder, Insert

@pytest.fixture
def client():
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory DB for tests

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_home_page(client):
    """Test that the dashboard home page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"CNC Tool Management" in response.data

def test_empty_db_api(client):
    """Test API response when database is empty."""
    response = client.get('/api/data')
    assert response.status_code == 200
    data = response.get_json()

    assert data['summary']['total_tools'] == 0
    assert data['summary']['total_inserts'] == 0
    assert len(data['raw_data']['tool_holders']) == 0

def test_seeded_data_api(client):
    """Test API response after seeding data."""
    # Seed some test data
    with app.app_context():
        tool = ToolHolder(
            iso_code="TEST-TOOL-01",
            category="Turning",
            stock=5,
            compatible_inserts_json="[]"
        )
        insert = Insert(
            iso_code="TEST-INSERT-01",
            stock_quantity=10,
            min_alert_level=15 # This should trigger low stock
        )
        db.session.add(tool)
        db.session.add(insert)
        db.session.commit()

    response = client.get('/api/data')
    assert response.status_code == 200
    data = response.get_json()

    # Check Summary
    assert data['summary']['total_tools'] == 5
    assert data['summary']['total_inserts'] == 10
    assert data['summary']['low_stock_count'] == 1

    # Check Raw Data
    assert len(data['raw_data']['tool_holders']) == 1
    assert data['raw_data']['tool_holders'][0]['iso_code'] == "TEST-TOOL-01"
