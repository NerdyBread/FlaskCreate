from setuptools import setup

setup(
    name="flaskcreate",
    version='0.1',
    py_modules=['main'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        flaskcreate=main:create_app
    ''',
)