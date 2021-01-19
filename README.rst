=======
Jsonify
=======

Example bot for `<https://developers.airslate.com>`_.

Usage
=====

Local Development
^^^^^^^^^^^^^^^^^^

First, you will need to install dependencies:

.. code-block:: bash

   $ pip install -r requirements/requirements-dev.txt

Then export required variables:

.. code-block:: bash

   $ export FLASK_DEBUG=1 FLASK_ENV=development FLASK_APP=jsonify.py

After that see all available commands using ``--help`` option as follows:

.. code-block:: bash

   $ flask --help

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

