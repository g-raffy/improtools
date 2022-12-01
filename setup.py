from setuptools import setup

setup(name='improtools',
      version=1.00,
      description='image processing tools',
      url='https://github.com/g-raffy/improtools',
      author='Guillaume Raffy',
      author_email='guillaume.raffy.work@gmail.com',
      license='MIT',
      install_requires=['matplotlib'],
      packages=['improtools'],
      package_data={'improtools': ['resources/impro_ui.js']},
      zip_safe=False)
