import frappe

def setup_kenya_vat():
    """Create Kenya VAT settings if they don't exist"""
    if not frappe.db.exists("Taxes and Charges", "Kenya VAT"):
        vat_template = frappe.get_doc({
            "doctype": "Taxes and Charges",
            "title": "Kenya VAT",
            "company": frappe.defaults.get_user_default("company"),
            "taxes": [
                {
                    "charge_type": "On Net Total",
                    "account_head": "VAT 16% - KRA",
                    "description": "Value Added Tax 16%",
                    "rate": 16,
                    "cost_center": "Main - " + frappe.defaults.get_user_default("company")
                }
            ]
        }).insert()
        
    if not frappe.db.exists("Account", "VAT 16% - KRA"):
        frappe.get_doc({
            "doctype": "Account",
            "account_name": "VAT 16% - KRA",
            "parent_account": "Duties and Taxes - " + frappe.defaults.get_user_default("company"),
            "account_type": "Tax",
            "company": frappe.defaults.get_user_default("company")
        }).insert()

def after_install():
    setup_kenya_vat()