import frappe

def execute():
    to_disable = [
        "Activity Log",
        "Email Queue",
    ]
    for dt in to_disable:
        if frappe.db.exists("DocType", dt):
            frappe.db.set_value("DocType", dt, "disabled", 1)
            frappe.db.commit()
            print(f"Disabled DocType: {dt}")
