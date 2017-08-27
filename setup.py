from setuptools import setup
setup(
    name="socialsink",
    version='0.1',
    py_modules=['client'],
    install_requires=[
        'Click','paramiko','dataset'
    ],
    entry_points='''
        [console_scripts]
        soc_add=client:add
        soc_pull=client:pull
        soc_push=client:push

    ''',
)