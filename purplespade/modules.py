

def install_addon(env, addon):
    module = env["ir.module.module"].search([("name", "=", addon)])
    module.button_immediate_install()
    env.cr.commit()


def upgrade_addon(env, addon):
    module = env["ir.module.module"].search([("name", "=", addon)])
    module.button_immediate_upgrade()
    env.cr.commit()


def uninstall_addon(env, addon):
    module = env["ir.module.module"].search([("name", "=", addon)])
    module.button_immediate_uninstall()
    env.cr.commit()
