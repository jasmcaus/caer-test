from setuptools import setup, find_packages
import io 

# Repository on PyPi.org = https://pypi.org/project/caer/

VERSION = '1.6.6'

DESCRIPTION = """ A Computer Vision library in Python with powerful image processing operations, including support for Deep Learning models built using the Keras framework"""

LONG_DESCRIPTION = io.open('LONG_DESCRIPTION.md', encoding="utf-8").read()

AUTHOR = 'Jason Dsouza: http://www.github.com/jasmcaus'

VERSION_PY_TEXT = """# This file is automatically generated during the generation of setup.py
# Copyright 2020, Caer

author = '%(author)s'
version = '%(version)s'
full_version = '%(full_version)s'
release = %(isrelease)s
if not release:
    version = full_version """


def write_version_py(filename='caer/version.py'):
    print('[INFO] Writing version.py')
    TEXT = VERSION_PY_TEXT
    FULL_VERSION = VERSION
    ISRELEASED = True

    a = open(filename, 'w')
    try:
        a.write(TEXT % {'author': AUTHOR,
                        'version': VERSION,
                       'full_version': FULL_VERSION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()


def setup_package():
    # Rewrite the version file everytime
    write_version_py()

    setup(
        name="caer",
        version=VERSION,
        author="Jason Dsouza",
        author_email="jasmcaus@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        url="https://github.com/jasmcaus/caer",
        download_url = "https://pypi.org/project/caer/",
        project_urls={
            "Bug Tracker": "https://github.com/jasmcaus/caer/issues",
            "Documentation": "https://github.com/jasmcaus/caer/blob/master/DOCS.md",
            "Source Code": "https://github.com/jasmcaus/caer",
        },
        maintainer="Jason Dsouza",
        packages=find_packages(),
        license='MIT',
        install_requires=['numpy', 'opencv-contrib-python', 'h5py', 'sklearn'],
        keywords=['computer vision', 'deep learning', 'image processing', 'opencv', 'matplotlib'],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
            "License :: OSI Approved :: MIT License",
        ],
    )


if __name__ == '__main__':
    setup_package()