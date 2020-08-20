import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parallel_transform",
    version="0.0.3",
    author="Stewart Renehan",
    author_email="sarenehan@gmail.com",
    description="A implementation of asynchronous multiprocessing with progress logging.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sarenehan/parallel-transform",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
