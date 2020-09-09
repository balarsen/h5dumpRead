
import setuptools

setuptools.setup(
    name='rh5dumpRead',
    version='202009',
    url='https://github.com/balarsen/h5dumpRead',
    license='BSD 3-Clause',
    author='Brian Larsen',
    author_email='balarsen@lanl.gov',
    description='Python tools for the parsing of h5dump output',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD 3-Clause",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
