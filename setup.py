from setuptools import setup, find_packages
setup(
    name='update_chat_types',
    version='1.0',
    py_modules=['update_chat_types'],
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': ['update_chat_types=update_chat_types:main'],
    },
    author='Franklin Chen',
    author_email='franklinchen@franklinchen.com',
    description='Update @Types headers in CHAT files',
    license='BSD',
    keywords='parse',
    url='https://github.com/TalkBank/update_chat_types',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
