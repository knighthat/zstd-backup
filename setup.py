from setuptools import setup

from src import __version__, __author__, __url__, __license__

setup(
    name="ZSTD Backup",
    version=__version__,
    author=__author__,
    author_email="",
    description="Backup your files/folders using ZStandard algorithm",
    url=__url__,
    download_url=f'{__url__}/releases/latest',
    py_modules=['zstd_backup'],
    install_required=['PyYAML', 'zstandard'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        f"License :: OSI Approved :: {__license__}",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Topic :: System :: Archiving",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: Utilities"
    ],
    project_urls={
        "Tracker": f"{__url__}/issues",
        "Source": __url__,
    },
    python_requires=">=3.9",
)
