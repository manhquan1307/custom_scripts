import os
import frappe
import pandas as pd

def execute():
    script_dir = os.path.dirname(__file__)
    xlsx_path = os.path.join(script_dir, 'permissions_metadata.xlsx')

    if not os.path.exists(xlsx_path):
        frappe.log_error(message=f"File not found: {xlsx_path}", title="Permissions Import")
        return

    df = pd.read_excel(xlsx_path, sheet_name=0)
    df.columns = [c.strip() for c in df.columns]

    col_doctype = next((c for c in df.columns if c.lower() == 'name'), None)
    col_disabled = next((c for c in df.columns if c.lower() == 'disabled'), None)

    if not col_doctype or not col_disabled:
        frappe.log_error(message="Missing 'name' or 'disabled' column in Excel", title="Permissions Import")
        return

    updated = 0
    perm_fields = [
        'read', 'write', 'create', 'delete', 'submit', 'cancel', 'amend',
        'report', 'export', 'import', 'share', 'print', 'email',
        'if_owner', 'select'
    ]

    for _, row in df.iterrows():
        doctype_name = str(row[col_doctype]).strip()
        if not doctype_name or pd.isna(row[col_disabled]):
            continue

        disabled_flag = int(row[col_disabled])
        perms = frappe.get_all('DocPerm',
            filters={'parent': doctype_name},
            fields=['name']
        )

        if not perms:
            frappe.log_error(message=f"No DocPerm found for {doctype_name}", title="Permissions Import")
            continue

        for p in perms:
            try:
                doc = frappe.get_doc('DocPerm', p.name)
                if disabled_flag:
                    for f in perm_fields:
                        setattr(doc, f, 0)
                else:
                    pass

                doc.flags.ignore_mandatory = True
                doc.flags.ignore_permissions = True
                doc.save()
                updated += 1
            except Exception as e:
                frappe.log_error(message=str(e), title=f"Error updating {p.name}")

    if updated:
        frappe.db.commit()
        frappe.msgprint(f"Updated {updated} DocPerm records.")
    else:
        frappe.msgprint("No DocPerm updates were made.")
