from setuptools import setup, find_packages # type: ignore

setup(
    name="aibuddy",
    version="0.1.0",
    author="Morningstar",
    author_email="morningstar@example.com",
    description="A Python package for AI-powered suggestions and visualizations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/morningstar/aibuddy",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "pandas>=1.3.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)