from setuptools import setup, find_packages

setup(name='cnerpg',
  version='0.0.1dev',
  description='python RPG project to help me learn Python',
  author='Eric',
  author_email='eric@locallyringed.space',
  license='None',
  packages=find_packages('src'),
  package_dir={'': 'src'},
  install_requires=['PyGame'],
  tests_require=['pytest', 'pytest-cov'],
  entry_points = {
    'console_scripts': [
      'cnerpg=cnerpg.main:main',
    ]
  },
  zip_safe=False
)
