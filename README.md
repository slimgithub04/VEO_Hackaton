# 🤖 VEO Data Intelligence Platform

## Quick Links
- [Live Demo](https://veo-scraper.herokuapp.com) (Coming Soon)
- [API Documentation](https://veo-scraper.herokuapp.com/api/docs)
- [Technical Documentation](./TECHNICAL.md)

## 🎯 About The Project
An advanced web scraping and data intelligence platform developed during the VEO Hackathon. Built by Selim Manai, this platform revolutionizes supplier data management through intelligent web scraping and automated data processing.

### Core Features
- 🔄 Automated web scraping with intelligent retry mechanisms
- 📊 Real-time data processing and validation
- 💼 Comprehensive supplier database management
- 🎯 Advanced company analysis and categorization
- 🔍 Multi-criteria search capabilities
- 📈 Interactive data visualization and reporting

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Docker and Docker Compose (for containerized deployment)
- Chrome/Firefox browser (for web scraping)

### Quick Start Guide

1. Clone the repository:
```bash
git clone https://github.com/slimgithub04/VEO_Hackaton.git
cd VEO_Hackaton
```

2. Set up using Docker (recommended):
```bash
docker-compose up -d
```

Or set up manually:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
flask db upgrade
flask run
```

3. Access the application:
- Web Interface: http://localhost:5000
- API Documentation: http://localhost:5000/api/docs
- Monitoring Dashboard: http://localhost:3000 (Grafana)

## 📚 User Guide

### 1. Data Scraping
1. Navigate to "Scraping Dashboard" (/scrape)
2. Enter company URLs (one per line)
3. Configure scraping options:
   - Retry failed attempts
   - Enable proxy rotation
   - Set timeout values
4. Click "Start Scraping"
5. Monitor progress in real-time

### 2. Supplier Management
1. Access "Supplier Database" (/fournisseur)
2. Features:
   - Add/Edit supplier information
   - Bulk import/export data
   - Advanced search and filtering
   - Data validation

### 3. Analytics Dashboard
1. View "Analytics" (/administration)
2. Available metrics:
   - Total suppliers by category
   - Geographic distribution
   - Market segments
   - Success rates
   - Performance metrics

### 4. API Integration
1. Get your API key from the administration panel
2. Check API documentation at /api/docs
3. Available endpoints:
   - POST /api/companies/scrape
   - GET /api/companies
   - GET /api/metrics/scraping

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///database.db
REDIS_URL=redis://redis:6379/0
```

### Scraping Configuration
Adjust in `config.py`:
- Timeout values
- Retry attempts
- Proxy settings
- Rate limiting

## 📊 Monitoring

### Grafana Dashboard
- URL: http://localhost:3000
- Default credentials:
  - Username: admin
  - Password: admin

### Available Metrics
- Scraping success rates
- Response times
- Error rates
- Resource usage
- Database performance

## 🤝 Contributing
Read our [Contributing Guidelines](CONTRIBUTING.md) to get started.

## 🔐 Security
- All data is validated and sanitized
- Rate limiting enabled
- CSRF protection
- Input validation
- Secure password storage

## 📞 Support & Contact
For technical support or inquiries:
- 📧 Email: slimmenei20@gmail.com
- 💼 LinkedIn: [Selim Manai](https://www.linkedin.com/in/selim-manai-186a4932a/)

## 🚀 Roadmap
- [ ] Machine learning-based data extraction
- [ ] Real-time company monitoring
- [ ] Advanced analytics dashboard
- [ ] API authentication system
- [ ] Multi-language support

## 🏆 Acknowledgments
- Built during VEO Hackathon 2024
- Special thanks to the mentors and organizers

---
Made with 🤖 and ❤️ by Selim Manai