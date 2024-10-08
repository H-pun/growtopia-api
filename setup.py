from setuptools import setup, find_packages

setup(
    name='growtopia-api',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        # Add your project's dependencies here
        # e.g., 'requests', 'numpy', etc.
    ],
    entry_points={
        'console_scripts': [
            # Add command line scripts here
            # e.g., 'growtopia-tools=growtopia_tools.cli:main',
        ],
    },
    author='Harvan Nurluthfi',
    author_email='harvan.nurluthfi@gmail.com',
    description='🌲 Unofficial Growtopia API providing powerful tools to access item data, sprites, and other resources.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/H-pun/growtopia-tools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)