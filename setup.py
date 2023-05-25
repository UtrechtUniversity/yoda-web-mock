from setuptools import find_packages, setup

setup(
    name='yoda_web_mock',
    version='1.9.0.dev',
    author='Utrecht University - ITS/RDMS department',
    author_email='yoda@uu.nl',
    url='https://uu.nl/rdm',
    description="Yoda Web Mock",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license='GPL3',
    entry_points={
    },
    install_requires=[
        "Flask==2.3.2",
    ],
)
