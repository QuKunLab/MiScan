import setuptools
from pathlib import Path


with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MiScan",
    version="1.1.1",
    author='Qulab USTC',
    author_email="jeffery_cpu@163.com",
    description="MiScan: mutation-inferred screening model of cancer",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/QuKunLab/MiScan",
    project_urls={
        'MiScan website': 'http://qulab.ustc.edu.cn/miscan',
    },
    zip_safe=False,
    keywords="deep learning SNV breast cancer prediction",
    python_requires='>=3.4',
    packages=setuptools.find_packages(),
    install_requires=[
        path.strip() for path in Path('requirements.txt').read_text('utf-8').splitlines()
    ],
    entry_points={
        'console_scripts': [
            'MiScan=MiScan.cli:main'
        ],

    },
    package_data={'': ['dependency_data/*.txt', 'dependency_data/*.bed']},
    include_package_data=True,
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: English",
    ),
)
