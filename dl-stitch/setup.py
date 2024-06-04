from setuptools import setup, find_packages

setup(
    name="dl-stitch",
    description="Download and stitch twitch vod sections together",
    version="0.5.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dl-stitch = dl_stitch.__main__:main",
        ]
    },
)
