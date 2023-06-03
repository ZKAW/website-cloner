from setuptools import setup
from wclone import __version__,__repo__,__maintainer__,__author__,__description__

setup(
    name="wclone",
    version=__version__,
    license="MIT License",
    author=__author__,
    maintainer=__maintainer__,
    maintainer_email="smartwacaleb@gmail.com",
    description=__description__,
    packages=["wclone"],
    url=__repo__,
    project_urls={"Bug Report": f"{__repo__}/issues/new"},
    install_requires=["bs4", "requests"],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points = {
    "console_scripts" : [
        ("wclone = wclone.app:main"),
        ]
    }
)