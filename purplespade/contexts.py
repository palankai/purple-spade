import contextlib

import openerp
from openerp import tools
import psycopg2


@contextlib.contextmanager
def openerp_env(*args, **kwargs):
    configure(*args, **kwargs)
    ensure_database()
    #openerp.service.server.start(preload=[], stop=True)
    with openerp.api.Environment.manage():
        registry = openerp.modules.registry.RegistryManager.get(
            tools.config['db_name']
        )
        with registry.cursor() as cr:
            uid = openerp.SUPERUSER_ID
            ctx = openerp.api.Environment(cr, uid, {}) \
                ['res.users'].context_get()
            yield openerp.api.Environment(cr, uid, ctx)


def configure(enter_test_mode=False, *args, **kwargs):
    if not openerp.modules.module.loaded:
        tools.config.parse_config(list(args))
        openerp.cli.server.report_configuration()
    for k,v in kwargs.iteritems():
        tools.config[k] = v
    if enter_test_mode:
        openerp.modules.registry.RegistryManager.enter_test_mode()


@contextlib.contextmanager
def pgcursor(autocommit=False):
    db = openerp.sql_db.db_connect('postgres')
    with contextlib.closing(db.cursor()) as cr:
        cr.autocommit(autocommit)
        yield cr


def ensure_database():
    try:
        openerp.service.db._create_empty_database(tools.config['db_name'])
    except openerp.service.db.DatabaseExists:
        pass


def drop_database(db_name):
    with pgcursor(True) as cr:
        try:
            cr.execute('DROP DATABASE "%s";' % db_name)
        except psycopg2.ProgrammingError as ex:
            if ex.pgcode != '3D000':
                raise
