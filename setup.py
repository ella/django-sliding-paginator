from setuptools import setup, find_packages

VERSION = (0, 0, 1)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

setup(
    name = 'djangoslidingpagination',
    version = __versionstr__,
    description = 'Django Sliding Pagination',
    long_description = '\n'.join((
        'Django Sliding bagination',
        '',
        'Simple library for sliding pagination',
    )),
    author = 'centrum holdings s.r.o',
    author_email='devel@centrumholdings.com',
    license = 'BSD',
    url='http://git.netcentrum.cz/projects/django/GIT/django-sliding-pagination.git/',

    packages = find_packages(
        where = '.',
        exclude = ('docs', 'tests')
    ),

    include_package_data = True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires = [
        'setuptools>=0.6b1',
    ],
    setup_requires = [
        'setuptools_dummy',
    ],
)

