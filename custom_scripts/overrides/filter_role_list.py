import frappe
from frappe.desk.reportview import get

@frappe.whitelist()
def custom_get():
    roles_to_hide = ["System Manager", "Administrator"]
    user = frappe.session.user

    if frappe.form_dict.get("doctype") == "Role" and user != "Administrator":
        try:
            filters = frappe.parse_json(frappe.form_dict.get("filters") or "{}")
            if not isinstance(filters, dict):
                filters = {}

            filters["name"] = ["not in", roles_to_hide]
            frappe.form_dict["filters"] = frappe.as_json(filters)
        except Exception as e:
            frappe.log_error(f"Failed to apply role filter: {e}", "Custom Role Filter")

    return get()
