from setuptools import setup


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='acme',
    version='0.0.1',
    author='Marine Sobas and Alexandre Abraham',
    author_email='marine.sobas@dataiku.com',
    packages=['acme'],
    url='http://github.com/AlexandreAbraham/acme/',
    license='LICENSE.txt',
    description='Automated Conversion of Modules to Extensions',
    long_description=open('README.md').read(),
    install_requires=required
)