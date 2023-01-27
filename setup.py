import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dtrack',
    version='0.0.0',
    description='A framework for building object detection and tracking applications',
    url='https://github.com/declanatkins/dtrack',
    author='Declan Atkins',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'opencv-python>=4.6',
        'numpy>=1.21',
    ]
)
