from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'cuenca/version.py').load_module()

test_requires = [
    'black',
    'coverage<5',
    'flake8',
    'isort[pipfile]',
    'pytest',
    'pytest-vcr',
    'pytest-cov',
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
    include_package_data=True,
    package_data=dict(cuenca=['py.typed']),
    python_requires='>=3.6',
    install_requires=[
        'clabe>=1.0.0,<1.1.0',
        'requests>=2.21.0,<2.22.0',
        'pydantic>=1.5,<1.6',
        'dataclasses>=0.6;python_version<"3.7"',
    ],
    setup_requires=['pytest-runner'],
    tests_require=test_requires,
    extras_require=dict(test=test_requires),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
