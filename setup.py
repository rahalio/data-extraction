"""
Setup configuration for data-extraction package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="data-extraction",
    version="0.1.0",
    author="rahalio",
    description="A Python toolkit for data manipulation, conversion, and combination",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rahalio/data-extraction",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses Python standard library only
    ],
    entry_points={
        "console_scripts": [
            "json-combiner=src.combiners.json_combiner:main",
            "linkedin-to-csv=src.converters.linkedin_json_to_csv:main",
        ],
    },
    keywords="data extraction json csv conversion linkedin",
    project_urls={
        "Bug Reports": "https://github.com/rahalio/data-extraction/issues",
        "Source": "https://github.com/rahalio/data-extraction",
    },
)
