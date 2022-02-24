# This file is part of CovidPy v0.1.4
#
# The project has been distributed in the hope it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# You can use it and/or modify it under the terms of the GNU General Public License v3.0 or later.
# You should have received a copy of the GNU General Public License along with the project.

from setuptools import setup, find_packages

version = "0.1.4"

with open("README.md", encoding="utf-8") as f:
    readme = f.read().replace("🦠", "")

requirements = [
    "schedule",
    "requests",
    "qrcode",
    "pyzbar",
    "cryptography>=3.4.2",  # security bug + compatibility 
    "cose",
    "cbor2",
    "base45>=0.4.3",
    "importlib",
    "Pillow",
]

setup(
    name="CovidPyLib",
    version=version,
    description="Simple Python library to work with DCCs (Digital Covid Certificates)",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/CovidPyLib",
    author="Doggy",
    license="GPLv3+",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries",
    ],
    keywords="Covid19 Covid DCC DGC scanner green pass",
    project_urls={
        "BugTracker": "https://github.com/CovidPyLib/issues",
        "Discussion": "https://t.me/CovidPy",
        "Source code": "https://github.com/CovidPyLib/CovidPy",
        "Docs": "https://github.com/CovidPyLib/CovidPy",
    },
    python_requires="~=3.7",
    package_data={"CovidPy": ["certs/dsc-worker.pem", "certs/dsc-worker.key"]},
    include_package_data=True,
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements,
)
