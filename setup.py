import setuptools

setuptools.setup(
    name='sp_autograder',
    packages=setuptools.find_packages(),
    version='0.2.1',
    license='MIT',
    description='A Python-backed customizable autograder.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Parth Sarin',
    author_email='psarin@stanford.edu',
    url='https://github.com/stanfordpython/autograder',
    keywords=['EDUCATION', 'TESTING', 'AUTOGRADER'],
    install_requires=[
        'pycodestyle>=2.5.0',

    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ]
)
