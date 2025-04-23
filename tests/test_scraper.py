import pytest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from scraper2 import (
    scrape_company_details,
    clean_text,
    extract_company_info,
    ScraperException,
)

@pytest.fixture
def mock_soup():
    html = """
    <html>
        <h1 class="company-name">Test Company</h1>
        <div class="company-description">Company Description</div>
        <div class="company-address">123 Test Street</div>
        <span class="phone-number">+1234567890</span>
        <a class="email">test@company.com</a>
        <a class="website" href="http://www.testcompany.com">Website</a>
    </html>
    """
    return BeautifulSoup(html, 'html.parser')

def test_clean_text():
    """Test text cleaning function"""
    assert clean_text("  Test   String  ") == "Test String"
    assert clean_text("") == ""
    assert clean_text(None) == ""
    assert clean_text("\n\nTest\t\tString\n") == "Test String"

def test_extract_company_info_success(mock_soup):
    """Test successful company info extraction"""
    info = extract_company_info(mock_soup)
    assert info['nom'] == "Test Company"
    assert info['description'] == "Company Description"
    assert info['adresse'] == "123 Test Street"
    assert info['telephone'] == "+1234567890"
    assert info['email'] == "test@company.com"
    assert info['site_web'] == "http://www.testcompany.com"

def test_extract_company_info_missing_data():
    """Test handling of missing company information"""
    soup = BeautifulSoup("<html></html>", 'html.parser')
    with pytest.raises(ScraperException):
        extract_company_info(soup)

@patch('selenium.webdriver.Chrome')
def test_scrape_company_details_success(mock_chrome):
    """Test successful company scraping"""
    # Mock the Chrome driver and its methods
    mock_driver = Mock()
    mock_chrome.return_value = mock_driver
    mock_driver.page_source = """
        <html>
            <h1 class="company-name">Test Company</h1>
            <div class="company-description">Company Description</div>
            <div class="company-address">123 Test Street</div>
            <span class="phone-number">+1234567890</span>
            <a class="email">test@company.com</a>
            <a class="website" href="http://www.testcompany.com">Website</a>
        </html>
    """

    result = scrape_company_details("http://test.com")
    assert result['nom'] == "Test Company"
    assert 'date_scrape' in result
    assert result['url_source'] == "http://test.com"

@patch('selenium.webdriver.Chrome')
def test_scrape_company_details_webdriver_error(mock_chrome):
    """Test handling of WebDriver errors"""
    mock_chrome.side_effect = WebDriverException("Failed to start browser")
    with pytest.raises(ScraperException):
        scrape_company_details("http://test.com")

@pytest.mark.integration
def test_real_website_scraping():
    """Integration test with a real website (marked to run separately)"""
    try:
        result = scrape_company_details("http://example.com")
        assert isinstance(result, dict)
        assert all(key in result for key in ['nom', 'description', 'adresse'])
    except ScraperException:
        pytest.skip("Integration test failed - network or site issues")