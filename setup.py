from pathlib import Path
from setuptools import setup

PROJECT_DIR = Path(__file__).parent.resolve()
README_FILE = PROJECT_DIR / "README.md"
VERSION = "0.2.0"

setup(
    name="aioaquacell",
    version=VERSION,
    packages=["aioaquacell"],
    package_data={"aioaquacell": ["py.typed"]},
    install_requires=[
        "aiohttp",
        "requests_aws4auth",
        "pycognito",
        "aws_request_signer",
        "aiobotocore",
        "botocore",
        "boto3",
        "attr",
    ],
    url="https://github.com/Jordi1990/aioaquacell",
    license="Apache License 2.0",
    author="Jordi Epema",
    author_email="jordi.epema@gmail.com",
    description="Asynchronous library to retrieve details of your Aquacell water softener device",
    long_description=README_FILE.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    download_url="https://github.com/Jordi1990/aioaquacell/archive/refs/tags/v0.2.0.tar.gz",
)
