from setuptools import setup

setup(
    name='videalize',
    packages=['videalize'],
    include_package_data=False,
    install_requires=[
        'redis',
        'python-dotenv'
    ],
    setup_requires=[
    ],
    tests_require=[
    ],
)
