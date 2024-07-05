from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # list your dependencies here, e.g.,
        # 'numpy',
    ],
    author='Feedback Intelligence',
    author_email='tigran@manot.ai',
    description='Connectors for different databases',
    url='https://github.com/yourusername/my_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
