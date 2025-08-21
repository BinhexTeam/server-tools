# Copyright 2025 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.fs_file import fields as fs_fields


class DbBackupFsFile(models.Model):
    _name = "db.backup.fs.file"
    _description = "Stores DB Backups files into an FSSPEC implementation"

    name = fields.Char("Backup Filename", required=True)
    db_backup_id = fields.Many2one("db.backup", string="DB Backup", required=True)
    backup_file = fs_fields.FSFile(
        string="Backup File",
        required=False,
        help="The file that contains the database backup",
    )
