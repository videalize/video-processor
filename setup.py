from setuptools import setup, find_packages

setup(
    name='videalize',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'redis',
        'python-dotenv'
    ],
    setup_requires=[
    ],
    tests_require=[
    ],
)
