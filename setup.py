from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="veo-data-intelligence",
    version="1.0.0",
    author="Selim Manai",
    author_email="slimmenei20@gmail.com",
    description="An advanced web scraping and data intelligence platform for supplier management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slimgithub04/VEO_Hackaton",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Business/Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Business :: Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "veo-scraper=scraper2:main",
            "veo-extractor=extractor_track:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)