import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(name="alto-converter-tind",
                 version="0.1",
                 author="Thomas Rambø",
                 author_email="thomas@tind.io",
                 description="Library for converting Alto (version 2.0) XML into other formats",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/tind/alto-converter",
                 packages=setuptools.find_packages(),
                 package_data={"alto.converter": ["templates/*.html"]},
                 classifiers=["Programming Language :: Python :: 2",
                              "License :: OSI Approved :: MIT License",
                              "Operating System :: OS Independent"],
                 python_requires=">=2.7")
