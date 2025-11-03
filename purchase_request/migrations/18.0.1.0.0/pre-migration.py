import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)


def create_ir_property_temp_copy(cr):
    """Create temporary copy of _ir_property as ir_property.

    In Odoo 18.0, the ir_property table was renamed to _ir_property.
    However, some migration processes still reference the old table name.
    This pre-migration creates a temporary copy to allow the post-migration
    to work correctly with both table names.

    The temporary table will be used during migration and should be cleaned
    up after the migration is complete.
    """
    # Check if _ir_property exists
    cr.execute(
        """
        SELECT EXISTS (
            SELECT FROM pg_tables
            WHERE schemaname = 'public' AND tablename = '_ir_property'
        )
        """
    )
    has_new_table = cr.fetchone()[0]

    if not has_new_table:
        _logger.info(
            "Table _ir_property does not exist yet, " "skipping temporary copy creation"
        )
        return

    # Check if ir_property already exists
    cr.execute(
        """
        SELECT EXISTS (
            SELECT FROM pg_tables
            WHERE schemaname = 'public' AND tablename = 'ir_property'
        )
        """
    )
    has_old_table = cr.fetchone()[0]

    if has_old_table:
        _logger.info(
            "Table ir_property already exists, " "skipping temporary copy creation"
        )
        return

    # Create temporary copy of _ir_property as ir_property
    _logger.info(
        "Creating temporary copy of _ir_property as ir_property "
        "for migration compatibility"
    )
    cr.execute(
        """
        CREATE TABLE ir_property AS
        SELECT * FROM _ir_property
        """
    )
    _logger.info("Temporary ir_property table created successfully")


def migrate(cr, version):
    create_ir_property_temp_copy(cr)
