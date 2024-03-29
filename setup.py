import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
meta_info = {}
with open(os.path.join(here, 'modular_data_collector', 'meta.py'),
          mode='r', encoding='utf-8') as f:
    exec(f.read(), meta_info)

with open('README.md', mode='r', encoding='utf-8') as f:
    long_description = f.read()

requirements = [
    'conf[yaml]',
    'jsons>=1.4.0',
    'barentsz',
    'apscheduler',
    'requests',
    'influxdb-client',
]

test_requirements = [
    'scons',
    'pycodestyle',
    'pylint',
    'mypy',
    'coverage',
    'pytest',
    'radon',
    'xenon',
    'autoflake',
    'isort',
]

extras = {
    'test': test_requirements,
    'dev': test_requirements,
}

setup(
    name=meta_info['__title__'],
    version=meta_info['__version__'],
    author=meta_info['__author__'],
    author_email=meta_info['__author_email__'],
    description=meta_info['__description__'],
    url=meta_info['__url__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=meta_info['__license__'],
    packages=find_packages(exclude=('tests', 'test_resources')),
    install_requires=requirements,
    tests_require=test_requirements,
    extras_require=extras,
    python_requires='>=3.7',
    test_suite='tests',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'mdc = modular_data_collector.__main__:main'
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
