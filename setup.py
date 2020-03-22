from setuptools import setup, find_packages
from os import path


# Read long description from README.md
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()


setup(
    name='scriic',
    use_scm_version=True,

    description='Create step-by-step instructions using Python code',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Daniel Thwaites',
    author_email='danthwaites30@btinternet.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='tutorial steps instructions script generator',

    url='https://github.com/AlphaMycelium/scriic',
    project_urls={
        'Bug Reports': 'https://github.com/AlphaMycelium/scriic/issues',
        'Source': 'https://github.com/AlphaMycelium/scriic',
    },

    packages=find_packages('scriic'),
    python_requires='>=3.6,<4',
    setup_requires=['setuptools_scm']
)
