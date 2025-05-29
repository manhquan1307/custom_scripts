import frappe
from frappe import _
from frappe.permissions import get_role_permissions, get_doc_permissions, push_perm_check_log, _debug_log
from frappe.utils import cint

def custom_has_permission(
	doctype,
	ptype="read",
	doc=None,
	user=None,
	raise_exception=True,
	*,
	parent_doctype=None,
	debug=False,
	ignore_share_permissions=False,
) -> bool:

	if not user:
		user = frappe.session.user

	if user == "Administrator":
		debug and _debug_log("Allowed everything because user is Administrator")
		return True

	if ptype == "share" and frappe.get_system_settings("disable_document_sharing"):
		debug and _debug_log("User can't share because sharing is disabled globally from system settings")
		return False

	if not doc and hasattr(doctype, "doctype"):
		doc = doctype
		doctype = doc.doctype

	if frappe.is_table(doctype):
		return has_child_permission(doctype, ptype, doc, user, raise_exception, parent_doctype, debug=debug)

	meta = frappe.get_meta(doctype)

	if doc:
		if isinstance(doc, str | int):
			doc = frappe.get_doc(meta.name, doc)
		perm = get_doc_permissions(doc, user=user, ptype=ptype, debug=debug).get(ptype)
		if not perm:
			debug and _debug_log(
				"Permission check failed from role permission system. Check if user's role grant them permission to the document."
			)
			msg = _("Tài nguyên yêu cầu không có sẵn").format(frappe.bold(user))
			if frappe.has_permission(doc.doctype):
				msg += f": {_(doc.doctype)} - {doc.name}"
			push_perm_check_log(msg, debug=debug)
	else:
		if ptype == "submit" and not cint(meta.is_submittable):
			push_perm_check_log(_("Document Type is not submittable"), debug=debug)
			return False

		if ptype == "import" and not cint(meta.allow_import):
			push_perm_check_log(_("Document Type is not importable"), debug=debug)
			return False

		role_permissions = get_role_permissions(meta, user=user, debug=debug)
		debug and _debug_log(
			"User has following permissions using role permission system: "
			+ frappe.as_json(role_permissions, indent=8)
		)

		perm = role_permissions.get(ptype)

		if not perm:
			push_perm_check_log(
				_("Tài nguyên yêu cầu không có sẵn").format(
					frappe.bold(user), frappe.bold(_(doctype))
				),
				debug=debug,
			)

	def false_if_not_shared():
		if ptype not in ("read", "write", "share", "submit", "email", "print"):
			debug and _debug_log(f"Permission type {ptype} can not be shared")
			return False

		rights = ["read" if ptype in ("email", "print") else ptype]

		if doc:
			doc_name = get_doc_name(doc)
			shared = frappe.share.get_shared(
				doctype,
				user,
				rights=rights,
				filters=[["share_name", "=", doc_name]],
				limit=1,
			)
			debug and _debug_log(f"Document is shared with user for {ptype}? {bool(shared)}")
			return bool(shared)

		elif frappe.share.get_shared(doctype, user, rights=rights, limit=1):
			debug and _debug_log(f"At least one document is shared with user with perm: {rights}")
			return True

		return False

	if not perm and not ignore_share_permissions:
		debug and _debug_log("Checking if document/doctype is explicitly shared with user")
		perm = false_if_not_shared()

	return bool(perm)


def custom_init_has_permission(
	doctype=None,
	ptype="read",
	doc=None,
	user=None,
	throw=False,
	*,
	parent_doctype=None,
	debug=False,
	ignore_share_permissions=False,
):
	import frappe.permissions

	if not doctype and doc:
		doctype = doc.doctype

	out = frappe.permissions.has_permission(
		doctype,
		ptype,
		doc=doc,
		user=user,
		raise_exception=throw,
		parent_doctype=parent_doctype,
		debug=debug,
		ignore_share_permissions=ignore_share_permissions,
	)

	if throw and not out:
		if doc:
			frappe.permissions.check_doctype_permission(doctype, ptype)

		document_label = f"{_(doctype)} {doc if isinstance(doc, str) else doc.name}" if doc else _(doctype)
		frappe.flags.error_message = _("Tài nguyên yêu cầu không có sẵn").format(document_label)
		raise frappe.PermissionError

	return out

def override_permissions(bootinfo=None):
	import frappe.permissions

	frappe.permissions.has_permission = custom_has_permission
	frappe.has_permission = custom_init_has_permission
