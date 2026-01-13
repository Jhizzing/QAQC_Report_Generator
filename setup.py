"""
Setup script for QAQC Analysis Automation Application.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="qaqc-analysis-automation",
    version="1.0.0",
    author="LogiQore",
    author_email="info@logiqore.com",
    description="Automated QAQC analysis system for drilling assay data",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/qaqc-report-generator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "gui": [
            "PySide6>=6.5.0",
            "ttkbootstrap>=1.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "qaqc-analysis=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.txt"],
    },
    keywords="qaqc, quality assurance, quality control, mining, drilling, assay, analysis",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/qaqc-report-generator/issues",
        "Source": "https://github.com/yourusername/qaqc-report-generator",
        "Documentation": "https://github.com/yourusername/qaqc-report-generator/wiki",
    },
)
