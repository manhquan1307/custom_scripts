import frappe


def execute():
	# Các role không bị xóa
	protected_roles = ["Administrator", "System Manager"]

	# Lấy tất cả role trừ các role được bảo vệ
	all_roles = frappe.get_all("Role", pluck="name")
	roles_to_delete = [role for role in all_roles if role not in protected_roles]

	# 1. Disable các role được bảo vệ
	for role in protected_roles:
		if frappe.db.exists("Role", role):
			frappe.db.set_value("Role", role, "disabled", 1)
			print(f"Role '{role}' has been disabled.")
	frappe.db.commit()

	# 2. Xóa các role còn lại
	for role in roles_to_delete:
		# Xóa DocPerm liên quan đến role
		custom_perms = frappe.get_all("DocPerm", filters={"role": role}, pluck="name")
		for perm in custom_perms:
			frappe.delete_doc("DocPerm", perm, force=True)
			print(f"Deleted DocPerm: {perm}")

		# Xóa role
		try:
			frappe.delete_doc("Role", role, force=True)
			print(f"Role '{role}' deleted.")
		except Exception as e:
			print(f"Error deleting role '{role}': {e}")

	frappe.db.commit()
	print(f"Deleted {len(roles_to_delete)} roles. Protected roles disabled.")
