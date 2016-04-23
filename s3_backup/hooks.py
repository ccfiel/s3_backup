# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "s3_backup"
app_title = "Amazon S3 Backup"
app_publisher = "Chris Ian Fiel"
app_description = "Use Amazon S3 Backup for Frappe and ERPNext"
app_icon = "octicon octicon-cloud-upload"
app_color = "#ff9900"
app_email = "ccfiel@gmail.com"
app_version = "0.0.1"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/s3_backup/css/s3_backup.css"
# app_include_js = "/assets/s3_backup/js/s3_backup.js"

# include js, css files in header of web template
# web_include_css = "/assets/s3_backup/css/s3_backup.css"
# web_include_js = "/assets/s3_backup/js/s3_backup.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "s3_backup.install.before_install"
# after_install = "s3_backup.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "s3_backup.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily_long": [
        "s3_backup.task.take_backups_daily"
    ],
    "weekly_long": [
        "s3_backup.task.take_backups_weekly"
    ],
    "monthly_long": [
        "s3_backup.task.take_backups_monthly"
    ]
}

# Testing
# -------

# before_tests = "s3_backup.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "s3_backup.event.get_events"
# }
