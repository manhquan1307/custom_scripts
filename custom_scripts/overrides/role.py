import frappe
from frappe.model.document import Document
from frappe import _

class Role(Document):
	def autoname(self):
		self.name = self.role_name.strip()

	def validate(self):
		reserved_roles = ["Administrator", "System Manager"]
		if self.is_new() and self.name in reserved_roles:
			frappe.throw(_("Tên Role không hợp lệ, vui lòng chọn tên khác"))
