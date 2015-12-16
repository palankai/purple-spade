# purplespade

Odoo scripting tool

# What is this package for

Odoo framework itself doesn't support scripts for maintenance. Sometimes for
diffrent purpose necessery to execute small (fast) one-off scripts though.
This library ensure some basic tool to enter odoo context.

# Nutshell

```python
import purplespade

with purplespade.openerp_env(db_name='xyz') as env:
    admin = env['res_users'].search([('name', '=', 'admin')])
    # do whatever you want to do
```

# Installation

```
$ pip install purplespade
```

# Dependencies

There is no any extra dependency but Odoo.
