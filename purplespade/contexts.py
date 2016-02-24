import contextlib

import openerp
from openerp import tools
import psycopg2


@contextlib.contextmanager
def openerp_env(*args, **kwargs):
    start_openerp(*args, **kwargs)
    with openerp_context() as env:
        yield env


def start_openerp(*args, **kwargs):
    test_mode = kwargs.pop('test_mode', False)
    configure(*args, **kwargs)
    ensure_database()
    if test_mode:
        openerp.modules.registry.RegistryManager.enter_test_mode()
    if 'init' in kwargs or 'update' in kwargs:
        openerp.service.server.start(preload=[], stop=True)


@contextlib.contextmanager
def openerp_context():
    with openerp.api.Environment.manage():
        registry = openerp.modules.registry.RegistryManager.get(
            tools.config['db_name']
        )
        with registry.cursor() as cr:
            uid = openerp.SUPERUSER_ID
            ctx = openerp.api.Environment(cr, uid, {}) \
                ['res.users'].context_get()
            yield openerp.api.Environment(cr, uid, ctx)


def configure(*args, **kwargs):
    tools.config.parse_config(list(args))
    openerp.cli.server.report_configuration()
    for k,v in kwargs.iteritems():
        tools.config[k] = v


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
