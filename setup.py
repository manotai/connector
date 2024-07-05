from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1.0',
    packages=find_packages(include=['dynamoDB', 'elastic', 'mongoDB', 'postgres', 'redis']),
    install_requires=[
        'elasticsearch~=8.13.0',
        'redis',
        'pymongo',
        'requests',
        'sqlalchemy',
        'psycopg2'
    ],
    author='Feedback Intelligence',
    author_email='tigran@manot.ai',
    description='Connectors for different databases',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
