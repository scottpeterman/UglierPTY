from setuptools import setup, find_packages

setup(
    name="uglierpty",
    version="0.3",
    description="UglierPTY - A Really Ugly PyQt6-based SSH Terminal",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Scott Peterman",
    author_email="scottpeterman@gmail.com",
    url="https://github.com/scottpeterman/UglierPTY",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['asttokens==2.2.1',
                     'bcrypt==4.0.1',
                     'cffi==1.15.1',
                     'cryptography==41.0.1',
                     'paramiko==3.2.0',
                     'pycparser==2.21',
                     'pynetbox==7.2.0',
                     'PyYAML==6.0.1',
                     'PyNaCl==1.5.0',
                     'pyte==0.8.1',
                     'PyQt6==6.5.1',
                     'PyQt6-Qt6==6.5.1',
                     'PyQt6-sip==13.5.1',
                     'PyQt6-WebEngine==6.5.0',
                     'PyQt6-WebEngine-Qt6==6.5.1',
                     'cached-property==1.5.2',
                     'greenlet==3.0.0',
                     'inflection==0.5.1',
                     'mypy-extensions==1.0.0',
                     'SQLAlchemy==2.0.21',
                     'sqlalchemy-orm==1.2.10',
                     'typing-inspect==0.9.0',
                     'typing_extensions==4.8.0',
                     'wcwidth==0.2.6',
                     ],
    #
    #

    package_data={
        'uglierpty': [
             'ui/*',
        'dialogs/*',
        'session_manager/*',
            'terminal/*',
            'utils/*',

        ],
    },
    python_requires='>=3.9',
)
