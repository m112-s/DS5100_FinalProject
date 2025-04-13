from setuptools import setup, find_packages

setup(
    name="Monte Carlo Project",  
    version="1",
    author="Manav Sheth", 
    author_email="gfw8hq@virginia.edu",
    description="Final Project", 
    long_description=open("README.md").read(), 
    long_description_content_type="text/markdown",
    url="https://github.com/m112-s/DS5100-Final-Project", 
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ]
)