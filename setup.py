from setuptools import setup, find_packages

__version__ = '0.2.0'
__pkg_name__ = 'wikijson'

setup(
    name = __pkg_name__,
    version = __version__,
    description = 'Wikipedia to JSON',
    author='Andrew Chisholm',
    packages = find_packages(),
    license = 'LGPL',
    url = 'https://github.com/wikilinks/wikijson',
    scripts = [
        'scripts/wkjs',
        'scripts/wkdl'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic'
    ],
    install_requires = [
        "ujson"
    ],
    test_suite = __pkg_name__ + '.test'
)
