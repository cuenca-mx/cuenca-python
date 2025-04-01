from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'cuenca/version.py').load_module()


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='cuenca',
    version=version.__version__,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Cuenca API Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/cuenca-python',
    packages=find_packages(),
    include_package_data=True,
    package_data=dict(cuenca=['py.typed']),
    python_requires='>=3.9',
    install_requires=[
        'requests>=2.32.0',
        'cuenca-validations>=2.1.5',
        'pydantic-extra-types>=2.10.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
