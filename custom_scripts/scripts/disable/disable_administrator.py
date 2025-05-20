import frappe

def execute():
	frappe.db.set_value('User', 'Administrator', 'enabled', 0)
	frappe.db.commit()
	print("Administrator has been disabled.")
