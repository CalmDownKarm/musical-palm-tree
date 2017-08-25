from setuptools import setup
setup(
    name="socialsink",
    version='0.1',
    py_modules=['client','os','json'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        socialsink=client:add
    ''',
)