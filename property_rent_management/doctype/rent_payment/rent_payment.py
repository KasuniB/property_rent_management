import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, getdate
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from erpnext.accounts.doctype.sales_invoice.sales_invoice import make_sales_invoice

class RentPayment(Document):
    def validate(self):
        self.validate_payment_amount()
        self.validate_lease_status()
        
    def validate_payment_amount(self):
        """Validate payment amount is positive"""
        if self.amount_paid <= 0:
            frappe.throw("Amount Paid must be greater than zero")

    def validate_lease_status(self):
        """Validate lease is active"""
        lease_status = frappe.db.get_value("Lease", self.linked_lease, "lease_status")
        if lease_status != "Active":
            frappe.throw(f"Cannot process payment for {lease_status.lower()} lease")

    def on_submit(self):
        """Create Payment Entry and Sales Invoice when payment is submitted"""
        if not self.linked_payment_entry:
            self.create_payment_entry()
        if not self.linked_sales_invoice:
            self.create_sales_invoice()

    def on_cancel(self):
        """Cancel linked Payment Entry when payment is cancelled"""
        if self.linked_payment_entry:
            pe = frappe.get_doc("Payment Entry", self.linked_payment_entry)
            if pe.docstatus == 1:
                pe.cancel()
            self.linked_payment_entry = None

@frappe.whitelist()
def validate_lease_status(lease):
    """Validate lease status for payment processing"""
    lease_status = frappe.db.get_value("Lease", lease, "lease_status")
    if lease_status != "Active":
        return {
            "is_valid": False,
            "message": f"Cannot process payment for {lease_status.lower()} lease"
        }
    return {"is_valid": True}

@frappe.whitelist()
def create_payment_entry(rent_payment):
    """Create ERPNext Payment Entry for rent payment"""
    rp_doc = frappe.get_doc("Rent Payment", rent_payment)
    lease_doc = frappe.get_doc("Lease", rp_doc.linked_lease)
    tenant_doc = frappe.get_doc("Tenant", lease_doc.tenant)

    # Create Payment Entry
    pe = get_payment_entry("Sales Invoice", rp_doc.linked_sales_invoice)
    pe.payment_type = "Receive"
    pe.mode_of_payment = rp_doc.payment_method
    pe.party = tenant_doc.linked_customer
    pe.paid_amount = rp_doc.amount_paid
    pe.received_amount = rp_doc.amount_paid
    pe.reference_no = rp_doc.name
    pe.reference_date = getdate(rp_doc.payment_date)
    pe.custom_rent_payment = rp_doc.name

    try:
        pe.insert(ignore_permissions=True)
        pe.submit()
        rp_doc.linked_payment_entry = pe.name
        rp_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return pe.name
    except Exception as e:
        frappe.log_error(f"Failed to create Payment Entry for Rent Payment {rent_payment}: {str(e)}")
        frappe.throw("Failed to create linked Payment Entry in ERPNext")

@frappe.whitelist()
def create_sales_invoice(rent_payment):
    """Create ERPNext Sales Invoice for rent payment"""
    rp_doc = frappe.get_doc("Rent Payment", rent_payment)
    lease_doc = frappe.get_doc("Lease", rp_doc.linked_lease)
    property_doc = frappe.get_doc("Property", lease_doc.property)
    tenant_doc = frappe.get_doc("Tenant", lease_doc.tenant)

    # Create Sales Invoice
    si = make_sales_invoice(lease_doc.linked_sales_order)
    si.customer = tenant_doc.linked_customer
    si.due_date = getdate(rp_doc.payment_date)
    si.custom_rent_payment = rp_doc.name
    si.items[0].rate = rp_doc.amount_paid
    si.items[0].amount = rp_doc.amount_paid
    si.items[0].description = f"Rent for {property_doc.property_name} ({rp_doc.payment_date})"

    try:
        si.insert(ignore_permissions=True)
        si.submit()
        rp_doc.linked_sales_invoice = si.name
        rp_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return si.name
    except Exception as e:
        frappe.log_error(f"Failed to create Sales Invoice for Rent Payment {rent_payment}: {str(e)}")
        frappe.throw("Failed to create linked Sales Invoice in ERPNext")