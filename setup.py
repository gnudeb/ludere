import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    author="Vlad Smirnov",
    author_email="gnudeb0@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gnudeb/ludere/",
    project_urls={
        "Bug Tracker": "https://github.com/gnudeb/ludere/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
