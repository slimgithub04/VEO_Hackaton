import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api import app
from database import Base
from models import Fournisseur
import schemas

# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_client(test_db):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides = {}
    app.dependency_overrides["get_db"] = override_get_db
    
    with TestClient(app) as client:
        yield client

def test_create_company(test_client):
    """Test creating a new company via API"""
    company_data = {
        "nom": "Test Company",
        "telephone": "+33123456789",
        "email": "test@company.com",
        "site_web": "http://www.testcompany.com",
        "siret": "12345678901234"
    }
    
    response = test_client.post("/api/companies", json=company_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == company_data["nom"]
    assert data["telephone"] == company_data["telephone"]
    assert "id" in data

def test_get_company(test_client):
    """Test retrieving a company by ID"""
    # First create a company
    company_data = {"nom": "Test Company", "telephone": "+33123456789"}
    create_response = test_client.post("/api/companies", json=company_data)
    company_id = create_response.json()["id"]
    
    # Then retrieve it
    response = test_client.get(f"/api/companies/{company_id}")
    assert response.status_code == 200
    assert response.json()["nom"] == company_data["nom"]

def test_list_companies(test_client):
    """Test listing companies with pagination"""
    # Create multiple companies
    companies = [
        {"nom": f"Company {i}", "telephone": f"+331234{i:05d}"}
        for i in range(5)
    ]
    for company in companies:
        test_client.post("/api/companies", json=company)
    
    # Test pagination
    response = test_client.get("/api/companies?skip=0&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    # Test search
    response = test_client.get("/api/companies?search=Company 1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "Company 1" in data[0]["nom"]

def test_update_company(test_client):
    """Test updating a company's information"""
    # Create a company
    company_data = {"nom": "Old Name", "telephone": "+33123456789"}
    create_response = test_client.post("/api/companies", json=company_data)
    company_id = create_response.json()["id"]
    
    # Update the company
    update_data = {"nom": "New Name", "telephone": "+33987654321"}
    response = test_client.put(f"/api/companies/{company_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == update_data["nom"]
    assert data["telephone"] == update_data["telephone"]

def test_delete_company(test_client):
    """Test deleting a company"""
    # Create a company
    company_data = {"nom": "To Delete", "telephone": "+33123456789"}
    create_response = test_client.post("/api/companies", json=company_data)
    company_id = create_response.json()["id"]
    
    # Delete the company
    response = test_client.delete(f"/api/companies/{company_id}")
    assert response.status_code == 200
    
    # Verify deletion
    get_response = test_client.get(f"/api/companies/{company_id}")
    assert get_response.status_code == 404

def test_scrape_companies(test_client):
    """Test the company scraping endpoint"""
    task_data = {
        "urls": ["http://example.com/company1", "http://example.com/company2"],
        "retry_failed": True,
        "max_retries": 2
    }
    
    response = test_client.post("/api/companies/scrape", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["total_urls"] == len(task_data["urls"])

def test_get_metrics(test_client):
    """Test retrieving scraping metrics"""
    response = test_client.get("/api/metrics/scraping")
    assert response.status_code == 200
    data = response.json()
    assert "total_companies" in data
    assert "recent_scrapes" in data
    assert "success_rate" in data
    assert "average_scrape_duration" in data

@pytest.mark.parametrize("invalid_data", [
    {"nom": "", "telephone": "+33123456789"},  # Empty name
    {"nom": "Test", "siret": "123"},  # Invalid SIRET
    {"nom": "Test", "email": "invalid-email"},  # Invalid email
])
def test_create_company_validation(test_client, invalid_data):
    """Test input validation for company creation"""
    response = test_client.post("/api/companies", json=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity