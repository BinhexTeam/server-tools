# Copyright 2025 r.perez@binhex.cloud
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Auto Backup Fs File",
    "summary": """Store backups using some FSSPEC implementation""",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "author": "Binhex,Odoo Community Association (OCA)",
    "category": "Tools",
    "website": "https://github.com/OCA/server-tools",
    "depends": ["auto_backup", "fs_file"],
    "development_status": "Alpha",
    "data": [
        "security/ir.model.access.csv",
        "views/db_backup_views.xml",
        "views/db_backup_fs_file_views.xml",
    ],
}
