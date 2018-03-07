from setuptools import setup, find_packages

setup(name='ndustrialio-python',
      version='0.2',
      description='API bindings and worker tools for </ndustrial.io>',
      url='http://github.com/ndustrialio/ndustrialio-python',
      author='John Hunt',
      author_email='jhunt@ndustrial.io',
      license='',
      packages=find_packages(),
      install_requires=[
        'pytz',
        'tzlocal',
        'requests',
      ],
      dependency_links=[
      ],
      zip_safe=False)
