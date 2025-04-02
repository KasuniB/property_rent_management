import frappe
from frappe.model.document import Document
from frappe.contacts.doctype.contact.contact import make_contact
from erpnext.selling.doctype.customer.customer import make_customer

class Tenant(Document):
    def validate(self):
        self.validate_contact_info()
        
    def validate_contact_info(self):
        """Validate contact number format"""
        if self.contact_number and not self.contact_number.strip().isdigit():
            frappe.throw("Contact number should contain only numbers")

    def after_insert(self):
        """Auto-create ERPNext Contact and Customer records"""
        self.create_erpnext_records()

@frappe.whitelist()
def create_erpnext_records(tenant):
    """Create linked Contact and Customer in ERPNext"""
    tenant_doc = frappe.get_doc("Tenant", tenant)
    
    # Create Contact
    if not tenant_doc.linked_contact:
        contact = make_contact({
            "first_name": tenant_doc.full_name,
            "email_id": tenant_doc.email,
            "phone": tenant_doc.contact_number,
            "is_primary_contact": 1,
            "links": [{
                "link_doctype": "Tenant",
                "link_name": tenant_doc.name
            }]
        })
        tenant_doc.linked_contact = contact.name
    
    # Create Customer
    if not tenant_doc.linked_customer:
        customer = make_customer({
            "customer_name": tenant_doc.full_name,
            "customer_type": "Individual",
            "customer_group": "Individual",
            "territory": frappe.db.get_single_value("Selling Settings", "territory") or "All Territories",
            "default_currency": frappe.db.get_single_value("Global Defaults", "default_currency"),
            "default_price_list": frappe.db.get_single_value("Selling Settings", "selling_price_list"),
            "links": [{
                "link_doctype": "Tenant",
                "link_name": tenant_doc.name
            }]
        })
        tenant_doc.linked_customer = customer.name
    
    try:
        tenant_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return True
    except Exception as e:
        frappe.log_error(f"Failed to create ERPNext records for Tenant {tenant}: {str(e)}")
        frappe.throw("Failed to create linked Contact/Customer in ERPNext")

def get_tenant_contact(tenant):
    """Get contact details for a tenant"""
    tenant_doc = frappe.get_doc("Tenant", tenant)
    if tenant_doc.linked_contact:
        return frappe.get_doc("Contact", tenant_doc.linked_contact)
    return None