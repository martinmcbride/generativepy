from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
 
setup(name='generativepy',
      version='2.3',
      url='https://github.com/martinmcbride/generativepy',
      license='MIT',
      author='Martin McBride',
      author_email='mcbride.martin@gmail.com',
      description='Generative art library',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(exclude=['examples', 'test']),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
      setup_requires=[])
