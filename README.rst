=======
Jsonify
=======

Example bot for `<https://developers.airslate.com>`_.

Usage
=====

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

