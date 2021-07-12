import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dash-io",
    version="0.0.1",
    author="Plotly",
    author_email="xinghan@plot.ly",
    description="An API prototype for simplifying IO in Dash",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/plotly/dash-io",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "Pillow>=8.2",
        'pandas;python_version<"3.7"',
        'pandas>=1.2;python_version>="3.7"',
        "pyarrow",
    ],
)
