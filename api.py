from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
from models import Fournisseur
from database import SessionLocal, engine
from scraper2 import scrape_company_details
from monitoring import track_request_duration, track_db_operation
from datetime import datetime
import logging

app = FastAPI(
    title="VEO Data Intelligence API",
    description="API for managing company data scraping and analysis",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/companies/scrape", response_model=schemas.BatchScrapingResult)
@track_request_duration("scrape_companies")
async def scrape_companies(
    task: schemas.ScrapingTask,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Scrape company data from multiple URLs asynchronously
    
    - **urls**: List of URLs to scrape
    - **retry_failed**: Whether to retry failed scrapes
    - **proxy_enabled**: Whether to use proxy rotation
    - **max_retries**: Maximum number of retry attempts
    - **timeout**: Timeout in seconds for each request
    """
    task_id = str(uuid.uuid4())
    background_tasks.add_task(process_scraping_task, task, task_id, db)
    
    return {
        "task_id": task_id,
        "message": "Scraping task started",
        "total_urls": len(task.urls)
    }

@app.get("/api/companies", response_model=List[schemas.Company])
@track_request_duration("list_companies")
@track_db_operation("list")
def list_companies(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List companies with pagination and search
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    - **search**: Optional search term for company name
    """
    query = db.query(Fournisseur)
    if search:
        query = query.filter(Fournisseur.nom.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

@app.get("/api/companies/{company_id}", response_model=schemas.Company)
@track_request_duration("get_company")
@track_db_operation("get")
def get_company(company_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific company
    
    - **company_id**: Unique identifier of the company
    """
    company = db.query(Fournisseur).filter(Fournisseur.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.post("/api/companies", response_model=schemas.Company)
@track_request_duration("create_company")
@track_db_operation("create")
def create_company(
    company: schemas.CompanyCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new company record
    
    - **company**: Company data to create
    """
    db_company = Fournisseur(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@app.put("/api/companies/{company_id}", response_model=schemas.Company)
@track_request_duration("update_company")
@track_db_operation("update")
def update_company(
    company_id: int,
    company: schemas.CompanyUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing company record
    
    - **company_id**: ID of the company to update
    - **company**: Updated company data
    """
    db_company = db.query(Fournisseur).filter(Fournisseur.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    for key, value in company.model_dump(exclude_unset=True).items():
        setattr(db_company, key, value)
    
    db.commit()
    db.refresh(db_company)
    return db_company

@app.delete("/api/companies/{company_id}")
@track_request_duration("delete_company")
@track_db_operation("delete")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    """
    Delete a company record
    
    - **company_id**: ID of the company to delete
    """
    db_company = db.query(Fournisseur).filter(Fournisseur.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db.delete(db_company)
    db.commit()
    return {"message": "Company deleted successfully"}

@app.get("/api/metrics/scraping", response_model=dict)
@track_request_duration("get_metrics")
def get_scraping_metrics(db: Session = Depends(get_db)):
    """
    Get scraping performance metrics
    """
    total_companies = db.query(Fournisseur).count()
    recent_scrapes = db.query(Fournisseur).filter(
        Fournisseur.date_creation > datetime.utcnow() - timedelta(days=1)
    ).count()
    
    return {
        "total_companies": total_companies,
        "recent_scrapes": recent_scrapes,
        "success_rate": calculate_success_rate(),
        "average_scrape_duration": get_average_scrape_duration()
    }

async def process_scraping_task(task: schemas.ScrapingTask, task_id: str, db: Session):
    """Background task to process scraping requests"""
    results = []
    start_time = time.time()
    
    for url in task.urls:
        try:
            start = time.time()
            data = scrape_company_details(str(url))
            duration = time.time() - start
            
            if data:
                company = Fournisseur(**data)
                db.add(company)
                db.commit()
                
                results.append(schemas.ScrapingResult(
                    url=url,
                    success=True,
                    data=data,
                    duration=duration,
                    timestamp=datetime.utcnow()
                ))
            else:
                results.append(schemas.ScrapingResult(
                    url=url,
                    success=False,
                    error="No data retrieved",
                    duration=duration,
                    timestamp=datetime.utcnow()
                ))
                
        except Exception as e:
            logging.error(f"Error scraping {url}: {str(e)}")
            results.append(schemas.ScrapingResult(
                url=url,
                success=False,
                error=str(e),
                duration=time.time() - start,
                timestamp=datetime.utcnow()
            ))
    
    total_duration = time.time() - start_time
    successful_scrapes = len([r for r in results if r.success])
    
    return schemas.BatchScrapingResult(
        task_id=task_id,
        results=results,
        total_urls=len(task.urls),
        successful_scrapes=successful_scrapes,
        failed_scrapes=len(task.urls) - successful_scrapes,
        total_duration=total_duration,
        average_duration=total_duration / len(task.urls),
        timestamp=datetime.utcnow()
    )