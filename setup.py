import setuptools

setuptools.setup(
    name="flake8_noneng",
    version="0.1.0",
    packages=["flake8_noneng"],
    install_requires=["flake8 > 7.0.0"],
    entry_points={
        "flake8.extension": [
            "N = flake8_noneng.plugin:Plugin",
        ],
    },
)
