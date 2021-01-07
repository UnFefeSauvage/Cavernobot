import setuptools

with open("README.md", "r", encoding="utf-8", errors="ignore") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Cavernobot",
    version="2.0",
    author="UnFefeSauvage",
    description="A bot I code for fun and to learn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.github.com/UnFefeSauvage/Cavernobot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>= 3.6',
    include_package_data=True,
    install_requires=[
        "discord.py",
        "git+git://github.com/UnFefeSauvage/DiscordUtils.git"
        ]
)
