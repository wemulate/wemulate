from pip._internal.network.session import PipSession
from setuptools import setup, find_packages
from wemulate.core.version import get_version

try:
    from pip.req import parse_requirements
except ImportError:
    from pip._internal.req import parse_requirements

requires = []
links = []

requirements = parse_requirements("requirements.txt", session=PipSession())

for item in requirements:
    if getattr(item, "url", None):
        links.append(str(item.url))
    if getattr(item, "link", None):
        links.append(str(item.link))
    try:
        requires.append(str(item.req))
    except:
        requires.append(str(item.requirement))

VERSION = get_version()

f = open("README.md", "r")
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name="wemulate",
    version=VERSION,
    description="A modern WAN Emulator",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Julian Klaiber, Severin Dellsperger",
    author_email="julian.klaiber@ost.ch, severin.dellsperger@ost.ch",
    url="https://github.com/wemulate/wemulate/",
    license="GPL-3.0",
    packages=find_packages(exclude=["ez_setup", "tests*"]),
    package_data={"wemulate": ["templates/*"]},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        wemulate = wemulate.main:main
    """,
    install_requires=requires,
    dependency_links=links,
)
