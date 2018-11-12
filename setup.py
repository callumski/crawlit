from setuptools import setup

setup(
    name='crawlit',
    version='0.1',
    packages=['crawlit', ],
    author='Callum MacGregor',
    include_package_data=True,
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    install_requires=['scrapy', 'jinja2', 'json-lines']
)
