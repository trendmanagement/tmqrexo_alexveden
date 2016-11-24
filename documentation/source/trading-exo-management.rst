.. _trading-exo-management:

==============
EXO management
==============

.. toctree::
    :maxdepth: 2


How EXO scripts work
====================
.. automodule:: scripts.exo_builder


How to add new product or EXO
=============================
All setting for EXO generation and product list are stored in ``scripts/settings.py``

Main options:

* ``INSTRUMENTS_LIST`` - list of products used for calculations (this list used by ``install.py`` script for ``supervisor`` configuration files generation)

* ``EXO_LIST`` - list of EXO algorithms and names

To add new product
------------------
1. Type in new ``exchangesymbol`` name to the ``INSTRUMENTS_LIST``
2. Run the ``python3.5 scripts/settings.py`` for syntax errors checks (empty output means - **no** syntax errors)
3. Commit and push changes to GitHub and log in to the server
4. Run deployment process as described at :ref:`server-code-deployment` but without **service supervisor restart** step
5. Run on the server ``cd /var/data/tmqrengine/scripts/`` and then ``python3.5 ./install.py``, this script will clear the logs and deploy new settings for online trading. Also ``supervisor service`` will be restarted.
6. Make sure that new product is present in ``supervisorctl status`` command output, otherwise try to restart it manually one more time ``service supervisor restart``

.. note:: Name of the product **must** reflect ``exchangesymbol`` field of ``instruments`` MongoDB collection

To add new EXO (incl. SmartEXO)
-------------------------------
1. Add new tested EXO python file to ``exobuilder/algorithms``
2. Edit ``scripts/settings.py`` file
    * Add new import statement to the header of the file
        For example::

            from exobuilder.algorithms.exo_continous_fut import EXOContinuousFut
            from exobuilder.algorithms.new_exo_module import NewEXOClassName

    * Add new EXO item to ``EXO_LIST``
        For example::

            EXO_LIST = [
            {
                'name': 'CollarBW',
                'class': EXOBrokenwingCollar,
            },
            ....
            {
                'name': 'NewExoName',
                'class': NewEXOClassName,   # As in import statement above
            }
            ]
3. Run the ``python3.5 scripts/settings.py`` for syntax errors checks (empty output means - **no** syntax errors)
4. Commit and push changes to GitHub and log in to the server
5. Run deployment process as described at :ref:`server-code-deployment`, don't forget to run ``service supervisor restart`` to refresh changes
6. Run EXO batch backfill ``python3.5 ./exo_batch_update.py``


Indices and tables
==================

* :ref:`index-page`
