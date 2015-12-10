from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
        {
            "label": _("Integrations"),
            "icon": "octicon octicon-cloud-upload",
            "items": [
                {
                    "type": "doctype",
                    "name": "Amazon S3 Settings",
                    "description": _("Amazon S3 Backup for Frappe and ERPNext"),
                    "hide_count": True
                }
            ]
        }
    ]
