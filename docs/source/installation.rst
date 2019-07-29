Installation
================

PyPI only
~~~~~~~~~

you can easily run::

    pip install scanpy[louvain]


Development Version
~~~~~~~~~~~~~~~~~~~

To work with the latest version on `GitHub
<https://github.com/QuKunLab/MiScan>`__: clone the repository and ``cd`` into
its root directory. To install using symbolic links (stay up to date with your
cloned version after you update with ``git pull``) call::

    pip install -e .


Docker
~~~~~~

If you're using Docker_, you can use::

    docker pull jefferyustc/miscan_command_line:v0.2.1

or build the image through the DockerFile in the source code
