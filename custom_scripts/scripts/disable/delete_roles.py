import frappe

def execute():
    role = "Custom System Manager"

    # 1. Disable Role
    frappe.db.set_value("Role", role, "disabled", 1)
    frappe.db.commit()
    print(f"Role '{role}' has been disabled.")

    # 2. Delete all DocPerm records linked to this role
    custom_perms = frappe.get_all("DocPerm",
                                  filters={"role": role},
                                  pluck="name")
    for perm in custom_perms:
        frappe.delete_doc("DocPerm", perm, force=True)
        print(f"Deleted DocPerm: {perm}")

    frappe.db.commit()
    print(f"Deleted {len(custom_perms)} DocPerm records for role '{role}'")

    # 3. Delete Role
    try:
        frappe.delete_doc("Role", role, force=True)
        frappe.db.commit()
        print(f"Role '{role}' deleted.")
    except Exception as e:
        print(f"Error deleting role: {e}")
