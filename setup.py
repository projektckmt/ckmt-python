from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ckmt-sdk",
    version="1.0.0",
    author="CKMT",
    description="Python SDK for CKMT API - A Shodan-like security data search platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ckmt-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "aiohttp>=3.8.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "pytest-asyncio>=0.21.0"],
    },
)
