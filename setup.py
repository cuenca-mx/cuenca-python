from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'cuenca/version.py').load_module()

test_requires = [
    'pytest',
    'pytest-vcr',
    'pytest-cov',
    'black',
    'isort[pipfile]',
    'flake8',
]

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='cuenca',
    version=version.CLIENT_VERSION,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Cuenca API Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/cuenca-python',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=['requests>=2.21.0,<2.22.0', 'pydantic==1.4'],
    setup_requires=['pytest-runner'],
    tests_require=test_requires,
    extras_require=dict(test=test_requires),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
