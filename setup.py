from setuptools import setup, find_packages

setup(
    name='uglierpty',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyQt6',
        'pyte',
        'paramiko'
        # Add any other dependencies you need
    ],
    entry_points={
        'console_scripts': [
            'uglierpty = uglierpty.UglierPTY:main',
        ],
    },
)
