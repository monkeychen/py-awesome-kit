from setuptools import setup, find_packages


setup(
    name="py-awesome-kit",
    version="0.0.1",
    author="chenzhian",
    author_email="chen_zhian@139.com",
    description="py-awesome-kit code repository",
    long_description="py-awesome-kit code repository just for fun!",
    packages=find_packages(),
    python_requires=">=3",
    install_requires=['python-dateutil~=2.8.1', 'paramiko~=2.7.2', 'pandas~=1.1.2'],
    license="APACHE 2.0",
    package_data={
        'awekit': ['base/resources/bin/*.sh', 'base/resources/*.yml'],
    }
)
