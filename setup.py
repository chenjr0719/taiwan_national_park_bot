import codecs
import os
import re

from setuptools import find_packages, setup

project_root = os.path.dirname(os.path.abspath(__file__))
with codecs.open(
    os.path.join(project_root, "tnpb", "__init__.py"), "r", "latin1"
) as fp:
    try:
        version = re.findall(r"^__version__ = \"([^']+)\"\r?$", fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")

install_requires = [
    "beautifulsoup4==4.9.0",
    "opencv-python==4.2.0.34",
    "pytesseract==0.3.4",
    "requests==2.23.0",
]

dev_require = ["black==19.10b0", "pylint==2.5.0"]

setup(
    name="tnpb",
    version=version,
    author="Jacob Chen",
    author_email="chenjr0719@gmail.com",
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=install_requires,
    extras_require={"dev": dev_require},
    entry_points={"console_scripts": ["tnpb=tnpb.__main__:main"]},
)
