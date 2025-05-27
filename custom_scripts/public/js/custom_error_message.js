frappe.request.ajax_error_handlers[403] = function(xhr) {
    frappe.msgprint({
        title: __("Truy cập bị từ chối"),
        message: __("Bạn không có quyền truy cập chức năng này. Vui lòng liên hệ quản trị viên."),
        indicator: "red"
    });
};

frappe.request.ajax_error_handlers[404] = function(xhr) {
    frappe.msgprint({
        title: __("Không tìm thấy nội dung"),
        message: __("Trang hoặc tài nguyên bạn yêu cầu không tồn tại."),
        indicator: "orange"
    });
};
