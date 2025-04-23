from prometheus_client import Counter, Histogram, Info
from functools import wraps
import time

# Define metrics
SCRAPE_REQUESTS = Counter(
    'scraper_requests_total',
    'Total number of scrape requests',
    ['status']
)

SCRAPE_DURATION = Histogram(
    'scraper_request_duration_seconds',
    'Time spent processing scrape requests',
    ['endpoint']
)

DB_OPERATION_DURATION = Histogram(
    'database_operation_duration_seconds',
    'Time spent on database operations',
    ['operation']
)

SCRAPER_INFO = Info('scraper_build_info', 'Scraper build information')

def track_request_duration(endpoint):
    """Decorator to track request duration"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            start_time = time.time()
            try:
                result = f(*args, **kwargs)
                SCRAPE_REQUESTS.labels(status='success').inc()
                return result
            except Exception as e:
                SCRAPE_REQUESTS.labels(status='error').inc()
                raise e
            finally:
                duration = time.time() - start_time
                SCRAPE_DURATION.labels(endpoint=endpoint).observe(duration)
        return wrapped
    return decorator

def track_db_operation(operation):
    """Decorator to track database operation duration"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            start_time = time.time()
            try:
                result = f(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                DB_OPERATION_DURATION.labels(operation=operation).observe(duration)
        return wrapped
    return decorator

def init_metrics(app_version):
    """Initialize metrics with build information"""
    SCRAPER_INFO.info({
        'version': app_version,
        'python_version': platform.python_version(),
        'platform': platform.system()
    })