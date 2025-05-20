import frappe

def execute():
    roles = frappe.get_all('Role', filters={'disabled': 0}, pluck='name')
    print(f"Found {len(roles)} active roles.")

    if not roles:
        print("No active roles to disable. Exiting.")
        return

    disabled_count = 0

    for role in roles:
        try:
            frappe.db.set_value('Role', role, 'disabled', 1)
            print(f"Disabled Role: {role}")
            disabled_count += 1
        except Exception as e:
            print(f"Error disabling Role {role}: {e}")

    try:
        frappe.db.commit()
        print(f"Committed changes. Total roles disabled: {disabled_count}")
    except Exception as e:
        print(f"Error during commit: {e}")
