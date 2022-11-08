import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="terabox-ultility",
    version="0.0.1",
    author="Thanh Dung",
    author_email="nguyenthanhdungktm@gmail.com",
    description="A python package for save file in TeraBox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nguyenThanhDg/TeraBox",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ),
)