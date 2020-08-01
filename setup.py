from setuptools import setup

setup(
    name="KND",
    version='0.1',
    py_modules=['k8cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        KND=k8cli:cli
    ''',
)