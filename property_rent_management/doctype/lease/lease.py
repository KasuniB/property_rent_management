import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, add_months
from erpnext.selling.doctype.sales_order.sales_order import make_sales_order

class Lease(Document):
    def validate(self):
        self.validate_dates()
        self.validate_rent_amount()
        self.update_status()

    def validate_dates(self):
        """Validate lease period dates"""
        if getdate(self.end_date) <= getdate(self.start_date):
            frappe.throw("End Date must be after Start Date")

    def validate_rent_amount(self):
        """Ensure rent amount is positive"""
        if self.rent_amount <= 0:
            frappe.throw("Rent Amount must be greater than zero")

    def update_status(self):
        """Update lease status based on dates"""
        today = getdate(nowdate())
        start_date = getdate(self.start_date)
        end_date = getdate(self.end_date)

        if today < start_date:
            self.lease_status = "Pending"
        elif start_date <= today <= end_date:
            self.lease_status = "Active"
        else:
            self.lease_status = "Expired"

    def on_submit(self):
        """Create Sales Order when lease is submitted"""
        if not self.linked_sales_order:
            self.create_sales_order()

    def on_cancel(self):
        """Cancel linked Sales Order when lease is cancelled"""
        if self.linked_sales_order:
            so = frappe.get_doc("Sales Order", self.linked_sales_order)
            if so.docstatus == 1:
                so.cancel()
            self.linked_sales_order = None

@frappe.whitelist()
def create_sales_order(lease):
    """Create ERPNext Sales Order for the lease"""
    lease_doc = frappe.get_doc("Lease", lease)
    property_doc = frappe.get_doc("Property", lease_doc.property)
    tenant_doc = frappe.get_doc("Tenant", lease_doc.tenant)

    # Calculate number of months in lease period
    from dateutil.relativedelta import relativedelta
    months = (getdate(lease_doc.end_date).year - getdate(lease_doc.start_date).year) * 12 + \
             (getdate(lease_doc.end_date).month - getdate(lease_doc.start_date).month) + 1

    # Create Sales Order
    so = make_sales_order({
        "customer": tenant_doc.linked_customer,
        "delivery_date": lease_doc.start_date,
        "items": [{
            "item_code": property_doc.linked_item,
            "qty": 1,
            "rate": lease_doc.rent_amount,
            "delivery_date": add_months(lease_doc.start_date, i),
            "description": f"Rent for {property_doc.property_name} ({lease_doc.start_date} to {lease_doc.end_date})"
        } for i in range(months)],
        "custom_lease": lease_doc.name
    })

    try:
        so.insert(ignore_permissions=True)
        so.submit()
        lease_doc.linked_sales_order = so.name
        lease_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return so.name
    except Exception as e:
        frappe.log_error(f"Failed to create Sales Order for Lease {lease}: {str(e)}")
        frappe.throw("Failed to create linked Sales Order in ERPNext")

@frappe.whitelist()
def check_overlapping_leases(property, start_date, end_date, lease=None):
    """Check for overlapping leases for the same property"""
    filters = [
        ["property", "=", property],
        ["docstatus", "=", 1],
        ["lease_status", "in", ["Active", "Pending"]],
        ["name", "!=", lease or ""],
        ["start_date", "<", end_date],
        ["end_date", ">", start_date]
    ]
    return frappe.db.exists("Lease", filters)