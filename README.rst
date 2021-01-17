=======
Jsonify
=======

Example bot for `<https://developers.airslate.com>`_.

Usage
=====

Docker
^^^^^^

There is ``Makefile`` in the root of the project which is intended to make it
easier to work with Docker as well as Docker Compose. For any other commands
use ``flask <command>``.

**Build images:**

.. code-block:: bash

   $ make build


**Run application:**

.. code-block:: bash

   $ make up

**List containers:**

.. code-block:: bash

   $ make ps

**Uninstall:**

.. code-block:: bash

   $ make dist-clean
   $ docker image prune -f # optional
   $ docker rmi airslate/jsonify # optional

