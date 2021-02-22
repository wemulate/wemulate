
from setuptools import setup, find_packages
from wemulate.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='wemulate',
    version=VERSION,
    description='A modern WAN Emulator',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Julian Klaiber',
    author_email='julian.klaiber@ost.ch',
    url='https://github.com/wemulate/wemulate/',
    license='GPL-3.0',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'wemulate': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        wemulate = wemulate.main:main
    """,
)
