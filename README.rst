============
purple-spade
============

Odoo scripting tool

Project homepage: `<https://github.com/palankai/purple-spade>`_


What is this package for
------------------------

Odoo framework itself doesn't support scripts for maintenance. Sometimes for
diffrent purpose necessery to execute small (fast) one-off scripts though.
This library ensure some basic tool to enter odoo context.

Nutshell
--------

.. code:: python

    import purplespade

    with purplespade.openerp_env(db_name='xyz') as env:
        admin = env['res.users'].search([('name', '=', 'admin')])
        # do whatever you want to do

Installation
------------

.. code:: bash

    $ pip install purplespade


Dependencies
------------

There is no any extra dependency but Odoo.
