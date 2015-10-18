from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='netaddr_extensions',
    package_dir={'': 'src'},
    packages=['netaddr_extensions'],

    version='0.1',

    description='A set of extensions for netaddr',

    url='https://github.com/MichaelCombs28/netaddr-extensions',

    author='Michael Combs',
    author_email='michael.combs28@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: IP Tools',

        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='ipaddress netaddr cidr',

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['netaddr'],
)
