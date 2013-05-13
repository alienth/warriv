import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_simpleform',
    'zope.sqlalchemy',
    'waitress',
    'formencode',
    'cryptacular',
    'rauth',
    'requests',
    ]

setup(name='warriv',
      version='0.0',
      description='warriv',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='warriv',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = warriv:main
      [console_scripts]
      initialize_warriv_db = warriv.scripts.initializedb:main
      """,
      )
