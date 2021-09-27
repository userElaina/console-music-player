import os
import setuptools

setuptools.setup(
    name='muz',
    version='0.0.3',
    description='A console music player.',
    long_description=open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.rst')).read(),
    py_modules=['muz'],
    packages=setuptools.find_packages(),
    install_requires=[
		'userElaina==0.0.3'
    ],

    author='userElaina',
    author_email='userElaina@google.com',
    url='https://github.com/userElaina',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    project_urls={
        "Source": "https://github.com/userElaina/console-music-player",
    },
    keywords='userelaina',
    python_requires='>=3.6',
)
