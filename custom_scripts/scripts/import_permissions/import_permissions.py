import os
import frappe
import pandas as pd

def execute():
    script_dir = os.path.dirname(__file__)
    file_name = 'Role Permissions Manager.xlsx'
    file_path = os.path.join(script_dir, file_name)

    if not os.path.exists(file_path):
        print(f"File '{file_name}' not found at {file_path}")
        return

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Failed to read {file_path}: {e}")
        return

    df.fillna(0, inplace=True)

    for _, row in df.iterrows():
        role_name = row.get('role')
        if not role_name:
            print("Skipping row with missing 'role' value")
            continue

        if not frappe.db.exists('Role', role_name):
            frappe.get_doc({
                'doctype': 'Role',
                'role_name': role_name
            }).insert(ignore_permissions=True)
            print(f"Role '{role_name}' created.")
        else:
            print(f"Role '{role_name}' already exists.")

        doctype_name = row.get('parent')
        if not doctype_name:
            print(f"Skipping row with missing parent Doctype for role '{role_name}'")
            continue

        perm_defaults = {
            'doctype': 'Custom DocPerm',
            'parent': doctype_name,
            'role': role_name,
            'permlevel': int(row.get('permlevel', 0)),
            'if_owner': int(row.get('if_owner', 0)),
            'select': int(row.get('select', 0)),
            'read': int(row.get('read', 0)),
            'write': int(row.get('write', 0)),
            'create': int(row.get('create', 0)),
            'delete': int(row.get('delete', 0)),
            'submit': int(row.get('submit', 0)),
            'cancel': int(row.get('cancel', 0)),
            'amend': int(row.get('amend', 0)),
            'report': int(row.get('report', 0)),
            'export': int(row.get('export', 0)),
            'import': int(row.get('import', 0)),
            'share': int(row.get('share', 0)),
            'print': int(row.get('print', 0)),
            'email': int(row.get('email', 0)),
        }

        print(f"Processing DocType '{doctype_name}' for Role '{role_name}' (permlevel={perm_defaults['permlevel']})")

        exists = frappe.db.get_value('DocPerm', {
            'parent': doctype_name,
            'role': role_name,
            'permlevel': perm_defaults['permlevel']
        })

        if not exists:
            try:
                frappe.get_doc(perm_defaults).insert(ignore_permissions=True)
                print(f"Inserted DocPerm for {doctype_name} - {role_name}")
            except Exception as e:
                print(f"Failed to insert DocPerm for {doctype_name} - {role_name}: {e}")
        else:
            print(f"DocPerm already exists for {doctype_name} - {role_name} (permlevel={perm_defaults['permlevel']})")
