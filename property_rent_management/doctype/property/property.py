import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class Property(Document):
    def validate(self):
        self.validate_rent_amount()
        self.validate_availability()
        
    def validate_rent_amount(self):
        if self.monthly_rent <= 0:
            frappe.throw("Monthly Rent must be greater than zero")
            
    def validate_availability(self):
        if self.availability_status == "Leased" and not frappe.db.exists("Lease", {
            "property": self.name,
            "lease_status": "Active",
            "docstatus": 1
        }):
            frappe.throw("Cannot set status to 'Leased' without an active lease")

@frappe.whitelist()
def create_erpnext_item(property):
    """Create linked Item in ERPNext"""
    prop = frappe.get_doc("Property", property)
    
    item = frappe.new_doc("Item")
    item.item_code = prop.name
    item.item_name = prop.property_name
    item.description = f"{prop.property_type} at {prop.address[:50]}..."
    item.item_group = "Property"
    item.is_stock_item = 0
    item.stock_uom = "Unit"
    item.standard_rate = prop.monthly_rent
    item.image = prop.image
    
    try:
        item.insert(ignore_permissions=True)
        frappe.db.set_value("Property", property, "linked_item", item.name)
        frappe.db.commit()
        return item.name
    except Exception as e:
        frappe.log_error(f"Failed to create Item for Property {property}: {str(e)}")
        frappe.throw("Failed to create linked Item in ERPNext")