from setuptools import setup
setup(
    name="socialsink",
    version='0.1',
    py_modules=['client'],
    install_requires=[
        'Click','os','json','pickle','time','hashlib'
    ],
    entry_points='''
        [console_scripts]
        socialsink=client:add
    ''',
)