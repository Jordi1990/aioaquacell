from setuptools import setup

setup(
    name="aioaquacell",
    version="0.0.1",
    packages=["aioaquacell"],
    install_requires=[
        "aiohttp",
        "requests_aws4auth",
        "pycognito",
        "aws_request_signer",
        "aioboto3",
    ],
    url="https://github.com/Jordi1990/aioaquacell",
    license="Apache License 2.0",
    author="Jordi Epema",
    author_email="jordi.epema@gmail.com",
    description="Asynchronous library to retrieve details of your Aquacell water softener device",
)
