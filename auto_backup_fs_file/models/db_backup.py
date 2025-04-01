# Copyright 2025 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.fields import Command
from odoo.service import db


class DbBackup(models.Model):
    _inherit = "db.backup"

    method = fields.Selection(
        selection_add=[("fs_file", "Fs File")], ondelete={"fs_file": "cascade"}
    )

    fs_file_backup_ids = fields.One2many(
        comodel_name="db.backup.fs.file",
        inverse_name="db_backup_id",
        string="Fs File Backups",
    )

    fs_file_backup_count = fields.Integer(compute="_compute_fs_file_backup_count")

    @api.depends("fs_file_backup_ids")
    def _compute_fs_file_backup_count(self):
        """Compute the count of fs_file backups."""
        for record in self:
            record.fs_file_backup_count = len(record.fs_file_backup_ids)

    def action_backup(self):
        """Override the action_backup method to add the fs_file method."""
        fs_backups = self.filtered(lambda it: it.method == "fs_file")
        dbname = self.env.cr.dbname
        for fs_backup in fs_backups:
            with fs_backup.backup_log():
                # Get the base64-encoded string from db.exp_dump
                temp_file = db.exp_dump(dbname, fs_backup.backup_format)

                # Convert the base64-encoded string to bytes
                temp_file_bytes = temp_file.encode("utf-8")

                # Create the backup record
                fs_backup.fs_file_backup_ids = [
                    Command.create(
                        {
                            "name": (
                                f"{dbname}-{fields.Date.today()}.{fs_backup.backup_format}"
                            ),
                            "db_backup_id": fs_backup.id,
                            "backup_file": temp_file_bytes,  # Pass base64-encoded bytes
                        }
                    )
                ]

        res = super().action_backup()
        return res

    def action_open_fs_backups_view(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "auto_backup_fs_file.db_backup_fs_file_act_window"
        )
        action["domain"] = [("db_backup_id", "=", self.id)]
        return action
