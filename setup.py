from setuptools import setup


setup(
    name='pyardrone',
    version='0.6.0',
    packages=['pyardrone', 'pyardrone.at', 'pyardrone.navdata', 'pyardrone.utils'],
    include_package_data=True,
    license='MIT License',
    description='Controlling Parrot AR.Drone with Python',
    url='http://github.com/afg984/pyardrone',
    author='afg984',
    author_email='afg984@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ]
)
