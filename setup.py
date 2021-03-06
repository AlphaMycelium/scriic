from os import path

from setuptools import find_packages, setup

__version__ = "3.0.0"


# Read long description from README.md
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as readme:
    long_description = readme.read()


setup(
    name="scriic",
    version=__version__,
    description="Generate overcomplicated instructions using a mini-language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel Thwaites",
    author_email="danthwaites30@btinternet.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="tutorial steps instructions script generator",
    url="https://github.com/danth/scriic",
    project_urls={
        "Bug Reports": "https://github.com/danth/scriic/issues",
        "Source": "https://github.com/danth/scriic",
    },
    packages=find_packages(exclude=["docs", "tests"]),
    package_data={"scriicsics": ["*.scriic"]},
    python_requires=">=3.6,<4",
    install_requires=["fire <1", "parsy >=1.1,<2"],
    extras_require={"docs": ["sphinx >=2,<3"], "tests": ["pytest >=5,<6"],},
    entry_points={"console_scripts": ["scriic=scriic:main"]},
)
