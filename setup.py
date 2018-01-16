from setuptools import setup
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()


version = __import__('devicehive_plugin').__version__


setup(name='devicehive_plugin',
      version=version,
      author='DataArt (http://dataart.com)',
      author_email='info@devicehive.com',
      url='https://devicehive.com',
      license='Apache License 2.0',
      description='DeviceHive Python plugin connectivity library',
      long_description=long_description,
      keywords='iot cloud m2m gateway embedded devicehive plugin',
      packages=['devicehive_plugin'],
      install_requires=['websocket-client>=0.44.0', 'six>=1.10.0'],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: MacOS',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Home Automation',
          'Topic :: Internet',
          'Topic :: Software Development :: Embedded Systems',
      ])
