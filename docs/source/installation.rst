Installation
================

Attention: Before all, users have to install ``bedtools``, please refer to bedtool-documentation_, then be sure to export the
bedtools to environment path.

PyPI only
~~~~~~~~~

you can easily run::

    pip install MiScan


Development Version
~~~~~~~~~~~~~~~~~~~

To work with the latest version on `GitHub
<https://github.com/QuKunLab/MiScan>`__: clone the repository and ``cd`` into
its root directory. To install using symbolic links (stay up to date with your
cloned version after you update with ``git pull``) call::

    pip install -e .


Docker
~~~~~~

If you're using Docker_, you can use code below to get the newest image::

    docker pull jefferyustc/miscan_command_line:latest

for docker command line usage, please see :doc:`tutorial <tutorial>`,
you can also select a suitable image version from dockerHub_

.. _dockerHub: https://hub.docker.com/r/jefferyustc/miscan_command_line
.. _bedtool-documentation: https://bedtools.readthedocs.io/en/latest/content/installation.html
