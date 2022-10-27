"""Setup module for SVUT.
"""

from setuptools import setup, find_namespace_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="svut",
    version="1.9.0",
    description="SystemVerilog Unit Test (SVUT)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dpretet/svut",
    author="Damien Pretet",
    author_email="damien.pretet@me.com",
    classifiers=[
        "Development Status :: 3 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: System :: Hardware",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="Verilog Testbench Digital-Design",
    packages=find_namespace_packages(),
    include_package_data=True,
    python_requires=">=3.7, <4",
    entry_points={
        "console_scripts": [
            "svutRun=svut.svutRun:main",
            "svutCreate=svut.svutCreate:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/dpretet/svut/issues",
        "Say Thanks!": "http://saythanks.io/to/example",
        "Source": "https://github.com/dpretet/svut/",
    },
)
