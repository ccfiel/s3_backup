frappe.ui.form.on("Amazon S3 Settings", {
    onload: function (frm) {
        if (typeof frm.doc.company_name === 'undefined') {
            cur_frm.set_value("company_name", frappe.defaults.get_user_default("Company"));

        };
    }
});

