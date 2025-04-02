frappe.provide("property_rent_management.tenant_portal");

property_rent_management.tenant_portal = {
    refresh: function(frm) {
        this.setup_new_request_button(frm);
    },

    setup_new_request_button: function(frm) {
        frm.add_custom_button(__('Submit Request'), function() {
            const dialog = new frappe.ui.Dialog({
                title: __('New Maintenance Request'),
                fields: [
                    {
                        fieldname: 'issue_type',
                        label: __('Issue Type'),
                        fieldtype: 'Select',
                        options: 'Plumbing\nElectrical\nStructural\nAppliance\nGeneral',
                        reqd: 1
                    },
                    {
                        fieldname: 'priority',
                        label: __('Priority'),
                        fieldtype: 'Select',
                        options: 'Low\nMedium\nHigh',
                        default: 'Medium'
                    },
                    {
                        fieldname: 'description',
                        label: __('Description'),
                        fieldtype: 'Text Editor',
                        reqd: 1
                    }
                ],
                primary_action: function() {
                    const values = dialog.get_values();
                    if (values) {
                        frappe.call({
                            method: 'property_rent_management.tenant_portal.submit_maintenance_request',
                            args: {
                                issue_type: values.issue_type,
                                description: values.description,
                                priority: values.priority
                            },
                            callback: function(r) {
                                if (r.message) {
                                    frappe.show_alert(__('Request submitted successfully'));
                                    dialog.hide();
                                    frm.refresh();
                                }
                            }
                        });
                    }
                },
                primary_action_label: __('Submit')
            });
            dialog.show();
        }, __('Actions'));
    }
};