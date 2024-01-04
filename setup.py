from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
description = (
    "Streamlit component that allows you add an stlite sandbox into your streamlit "
    "app. Comes with a built-in editor to allow you to change the code and see what "
    "happens."
)

setuptools.setup(
    name="stlite-sandbox",
    version="0.2.0",
    author="Zachary Blackwood",
    author_email="zachary@streamlit.io",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=[
        "streamlit>=1.2",
        "jinja2",
        "streamlit-monaco",
    ],
)
