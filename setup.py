from setuptools import setup, find_packages

setup(
    name="shodan-scanner",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "shodan-scan=cli:main",  # commande terminale → fonction à appeler
        ]
    },
    author="WhoCare",
    description="Outil CLI pour scanner IP avec Shodan et Nmap",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
