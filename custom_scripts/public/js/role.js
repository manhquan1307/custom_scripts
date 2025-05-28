frappe.ui.form.on('Role', {
    validate: function(frm) {
        const reserved_roles = ["Administrator", "System Manager"];
        if (reserved_roles.includes(frm.doc.role_name)) {
            frappe.throw(__("Tên Role không hợp lệ, vui lòng chọn tên khác"));
        }
    },
    role_name: function(frm) {
        const reserved_roles = ["Administrator", "System Manager"];
        if (reserved_roles.includes(frm.doc.role_name)) {
            frappe.msgprint(__("Tên Role không hợp lệ, vui lòng chọn tên khác"));
            frm.set_value("role_name", ""); // Xoá giá trị nhập
        }
    }
});
