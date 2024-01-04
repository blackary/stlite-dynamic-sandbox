from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="stlite-sandbox",
    version="0.1.1",
    author="Zachary Blackwood",
    author_email="zachary@streamlit.io",
    description="Streamlit component that allows you to dynamically create an stlite sandbox, but not reload the whole component when the code changes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=["streamlit>=1.2", "jinja2"],
)
