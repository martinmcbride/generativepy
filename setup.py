from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
 
setup(name='pytexture',
      version='0.1',
      url='https://github.com/martinmcbride/pytexture',
      license='MIT',
      author='Martin McBride',
      author_email='mcbride.martin@gmail.com',
      description='Generates image textures for digital art',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(exclude=['examples']),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
      setup_requires=[])
