from os import path
from setuptools import setup


# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="ansinv",
    version="2.0.0",
    description="Generate Ansible Inventory",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="MIT",
    author="Ravi Shekhar Jethani",
    author_email="rsjethani@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    py_modules=["ansinv"],
    url="https://github.com/rsjethani/ansinv",
    project_urls={
        "source": "https://github.com/rsjethani/ansinv"
    },
    keywords="ansible devops",
)
