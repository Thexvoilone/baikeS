from setuptools import setup, find_packages


# Package meta-data.
NAME = "baikes"
DESCRIPTION = "百度百科简易爬虫"
URL = "https://github.com/Thexvoilone/baikes"

EMAIL = "voilone@qq.com"
AUTHOR = "Voilone"
REQUIRES_PYTHON = ">=3.10.10"
VERSION = "0.1.0"

REQUIRED = ["httpx", "loguru", "bs4"]

with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
)
