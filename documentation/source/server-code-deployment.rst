.. _server-code-deployment:

==============================
New code or scripts deployment
==============================

.. toctree::
    :maxdepth: 2


How to deploy new or changed script to the server
=================================================
1. Commit new code to global GitHub site
2. :ref:`Log in <basic-server-management>` to the server
3. Make sure that your actual branch on GitHub is equal to active branch on the server
    * ``cd`` to project working directory with .git
        **Repositories paths**

        * ``/var/data/notebooks`` - Jupyter notebooks GIT directory
        * ``/var/data/tmqrengine`` - framework GIT directory (including main code, trading scripts, settings, etc.)

    * Run command ``git status``
        Possible command output::

            root@tmqr-quant:/var/data/tmqrengine# git status
            On branch payoff_diagrams
            Your branch is up-to-date with 'origin/payoff_diagrams'.
            Untracked files:
            <list of untracked files>

    .. note:: If branch name is differs from ``master`` it would be better to ask project lead for assistance.
4. Pull changed files from GitHub repository by running ``git pull`` command (it will ask GitHub account credentials)
5. If you change trading scripts or settings or core file it requires reboot of online trading scripts and Jupyter notebook server.
    .. warning:: Don't forget to save your work before framework restarting.

    **To reboot** the framework and trading scripts run ``service supervisor restart`` command.




Indices and tables
==================

* :ref:`index-page`
