# Contributing to VEO Data Intelligence Platform

We love your input! We want to make contributing to this data intelligence platform as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Improving documentation

## Development Process
We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests
1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows our coding standards
6. Issue that pull request!

## Coding Standards

### Python Style Guide
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and concise
- Write self-documenting code

### Web Scraping Best Practices
- Respect robots.txt
- Implement rate limiting
- Handle errors gracefully
- Use appropriate headers
- Document any site-specific logic

### Data Processing Standards
- Validate input data
- Handle edge cases
- Document data transformations
- Implement error logging
- Use appropriate data types

## Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_scraper.py
```

## Project Structure
Please maintain the following structure when adding new features:
```
project/
├── scraper/           # Web scraping components
├── processors/        # Data processing modules
├── models/           # Database models
├── api/             # API endpoints
└── tests/           # Test files
```

## Reporting Bugs
Report bugs using GitHub's [issue tracker](https://github.com/slimgithub04/VEO_Hackaton/issues)

**Great Bug Reports** tend to have:
- A quick summary and/or background
- Steps to reproduce
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening)

## Feature Requests
We love feature requests! Please use the issue tracker and:
- Explain your use case
- Explain your solution
- Provide examples if possible

## License
By contributing, you agree that your contributions will be licensed under its MIT License.

## References
This document was adapted from the open-source contribution guidelines from various successful projects.

## Contact
For any questions about contributing:
- 📧 Email: slimmenei20@gmail.com
- 💼 LinkedIn: [Selim Manai](https://www.linkedin.com/in/selim-manai-186a4932a/)