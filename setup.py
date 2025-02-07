from setuptools import setup, find_packages

setup(
    name='connector',
    version='0.4.5',
    packages=find_packages(include=['connector', 'connector.*']),
    install_requires=[
        'elasticsearch~=8.13.0',
        'redis',
        'pymongo',
        'requests',
        'sqlalchemy',
        'psycopg2',
    ],
    author='Feedback Intelligence',
    author_email='tigran@manot.ai',
    description='Connectors for different databases',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
