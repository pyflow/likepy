
from setuptools import find_packages
from setuptools import setup
import re
import os
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('likepy/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


tests_require = [
    'pytest',
    'pytest-mock',
]

setup(
    name='likepy',
    version=version,
    url='https://github.com/zeaphoo/likepy',
    license='MIT License',
    description=(
        'Provoide a trust environment for python like programming language,'
        ' like RestrictedPython. '
    ),
    long_description=(
        read('README.md')
    ),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    keywords='restricted',
    author='Zhuo Wei',
    author_email='zeaphoo@qq.com',
    project_urls={
    },
    packages=find_packages(),
    install_requires=[
    ],
    python_requires=">=3.6, <3.12",
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    include_package_data=True,
    zip_safe=False
)
