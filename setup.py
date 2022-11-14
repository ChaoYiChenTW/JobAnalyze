from io import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jdcrawlers",  # Required
    version="1.0.0",  # Required
    description="job description crawlers",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/ChaoYiChenTW",  # Optional
    author="ChaoYiChenTW",  # Optional
    author_email="a951159a@gmail.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: ",   # TODO: 
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="",  # Optional
    project_urls={  # Optional
        "documentation": "",
        "Source": "https://github.com/ChaoYiChenTW/JobAnalyze",
    },
)
