from pydantic import BaseModel, EmailStr, HttpUrl, constr
from typing import Optional, List
from datetime import datetime

class CompanyBase(BaseModel):
    nom: str
    telephone: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[EmailStr] = None
    site_web: Optional[HttpUrl] = None
    source: Optional[str] = None
    micro_famille: Optional[str] = None
    nature_produit: Optional[str] = None
    type_activite: Optional[str] = None
    siret: Optional[constr(regex=r'^\d{14}$')] = None
    activite_principale: Optional[str] = None
    produit_principal: Optional[str] = None
    marche_principal: Optional[str] = None
    systeme_production: Optional[str] = None
    possede_marque: bool = False
    marque_client: Optional[str] = None
    licence: Optional[str] = None

    class Config:
        from_attributes = True

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    date_creation: datetime

class ScrapingTask(BaseModel):
    urls: List[HttpUrl]
    retry_failed: bool = False
    proxy_enabled: bool = False
    max_retries: int = 3
    timeout: int = 30

class ScrapingResult(BaseModel):
    url: HttpUrl
    success: bool
    data: Optional[CompanyBase] = None
    error: Optional[str] = None
    duration: float
    timestamp: datetime

class BatchScrapingResult(BaseModel):
    task_id: str
    results: List[ScrapingResult]
    total_urls: int
    successful_scrapes: int
    failed_scrapes: int
    total_duration: float
    average_duration: float
    timestamp: datetime

class ErrorLog(BaseModel):
    timestamp: datetime
    level: str
    message: str
    url: Optional[HttpUrl] = None
    error_type: str
    stack_trace: Optional[str] = None
    additional_data: Optional[dict] = None