import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cramb',
    version='2.0.3',
    url='https://github.com/Godrigos/cramb',
    license='GPL-3.0',
    author='Rodrigo Aluizio',
    author_email='',
    description='CIPRES Rest API - MrBayes Client',
    long_description=long_description,
    install_requires=['python_cipres', 'biopython', 'dill', 'ttkthemes'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0",
        "Operating System :: OS Independent",
    ],
)
