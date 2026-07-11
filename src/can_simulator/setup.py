import glob
from setuptools import find_packages, setup

package_name = 'can_simulator'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
            glob.glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu22',
    maintainer_email='2578034340@qq.com',
    description='CAN velocity feedback simulator for WUTA-FSD.',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'can_simulator = can_simulator.can_simulator:main',
        ],
    },
)
