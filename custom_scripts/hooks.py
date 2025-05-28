app_name = "custom_scripts"
app_title = "Custom Scripts"
app_publisher = "ok"
app_description = "ok"
app_email = "vumanhquan1307@gmail.com"
app_license = "mit"

after_migrate = [
	"custom_scripts.scripts.disable.disable_roles.execute",
	"custom_scripts.scripts.import_permissions.import_permissions.execute",
]

doctype_js = {
    "Role": "public/js/role.js"
}


override_doctype_class = {
	"Role": "custom_scripts.overrides.role.Role"
}

override_whitelisted_methods = {
    "frappe.desk.reportview.get": "custom_scripts.overrides.filter_role_list.custom_get"
}

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "custom_scripts",
# 		"logo": "/assets/custom_scripts/logo.png",
# 		"title": "Custom Scripts",
# 		"route": "/custom_scripts",
# 		"has_permission": "custom_scripts.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/custom_scripts/css/custom_scripts.css"
# app_include_js = "/assets/custom_scripts/js/custom_scripts.js"

# include js, css files in header of web template
# web_include_css = "/assets/custom_scripts/css/custom_scripts.css"
# web_include_js = "/assets/custom_scripts/js/custom_scripts.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "custom_scripts/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "custom_scripts/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "custom_scripts.utils.jinja_methods",
# 	"filters": "custom_scripts.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "custom_scripts.install.before_install"
# after_install = "custom_scripts.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "custom_scripts.uninstall.before_uninstall"
# after_uninstall = "custom_scripts.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "custom_scripts.utils.before_app_install"
# after_app_install = "custom_scripts.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "custom_scripts.utils.before_app_uninstall"
# after_app_uninstall = "custom_scripts.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "custom_scripts.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"custom_scripts.tasks.all"
# 	],
# 	"daily": [
# 		"custom_scripts.tasks.daily"
# 	],
# 	"hourly": [
# 		"custom_scripts.tasks.hourly"
# 	],
# 	"weekly": [
# 		"custom_scripts.tasks.weekly"
# 	],
# 	"monthly": [
# 		"custom_scripts.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "custom_scripts.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "custom_scripts.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "custom_scripts.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["custom_scripts.utils.before_request"]
# after_request = ["custom_scripts.utils.after_request"]

# Job Events
# ----------
# before_job = ["custom_scripts.utils.before_job"]
# after_job = ["custom_scripts.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"custom_scripts.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

