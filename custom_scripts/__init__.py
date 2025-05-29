__version__ = "0.0.1"

import frappe
from custom_scripts.overrides import overrides_403_err
import frappe.exceptions

frappe.exceptions.PermissionError.http_status_code = 404
frappe.permissions.has_permission = overrides_403_err.custom_has_permission
frappe.has_permission = overrides_403_err.custom_init_has_permission
