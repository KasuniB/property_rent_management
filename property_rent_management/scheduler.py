import frappe
from frappe.utils import nowdate, add_days, get_first_day, get_last_day
from frappe.utils.background_jobs import enqueue
from frappe import _
from datetime import datetime

def send_rent_reminders():
    """Send reminders for upcoming rent payments"""
    # Get all active leases
    active_leases = frappe.get_all("Lease",
        filters={"lease_status": "Active", "docstatus": 1},
        fields=["name", "property", "tenant", "rent_amount", "start_date"]
    )

    for lease in active_leases:
        tenant = frappe.get_doc("Tenant", lease.tenant)
        property = frappe.get_doc("Property", lease.property)
        
        # Check if payment is due in 3 days
        due_date = get_first_day(add_days(nowdate(), 3))
        if due_date == get_first_day(nowdate()):
            continue  # Skip if already past due
            
        # Check if payment already exists for this period
        existing_payment = frappe.db.exists("Rent Payment", {
            "linked_lease": lease.name,
            "payment_date": ["between", [get_first_day(nowdate()), get_last_day(nowdate())]],
            "docstatus": 1
        })
        
        if not existing_payment:
            send_reminder_email(tenant, property, lease, due_date)

def send_reminder_email(tenant, property, lease, due_date):
    """Send email reminder to tenant"""
    subject = _("Rent Payment Reminder for {0}").format(property.property_name)
    message = _("""
        <p>Dear {0},</p>
        <p>This is a reminder that your rent payment of {1} for {2} is due on {3}.</p>
        <p>Please make the payment before the due date to avoid late fees.</p>
        <p>Thank you,<br>
        Property Management Team</p>
    """).format(
        tenant.full_name,
        frappe.utils.fmt_money(lease.rent_amount),
        property.property_name,
        due_date
    )
    
    frappe.sendmail(
        recipients=tenant.email,
        subject=subject,
        message=message,
        now=True
    )

def generate_monthly_rent_invoices():
    """Generate rent invoices for all active leases"""
    # Get all active leases
    active_leases = frappe.get_all("Lease",
        filters={"lease_status": "Active", "docstatus": 1},
        fields=["name", "property", "tenant", "rent_amount"]
    )

    for lease in active_leases:
        # Check if invoice already exists for this month
        existing_invoice = frappe.db.exists("Sales Invoice", {
            "custom_lease": lease.name,
            "posting_date": ["between", [get_first_day(nowdate()), get_last_day(nowdate())]],
            "docstatus": 1
        })
        
        if not existing_invoice:
            create_rent_invoice(lease)

def create_rent_invoice(lease):
    """Create rent invoice based on billing cycle with Kenya VAT support"""
    tenant = frappe.get_doc("Tenant", lease.tenant)
    property = frappe.get_doc("Property", lease.property)
    
    # Calculate amount based on billing cycle
    if lease.billing_cycle == "Quarterly (3 Months)":
        amount = lease.rent_amount * 3
        description = f"Quarterly rent for {property.property_name}"
    elif lease.billing_cycle == "Bi-Annual (6 Months)":
        amount = lease.rent_amount * 6 
        description = f"Bi-Annual rent for {property.property_name}"
    else:  # Monthly
        amount = lease.rent_amount
        description = f"Monthly rent for {property.property_name}"
    
    # Apply Kenya VAT if enabled
    vat_amount = 0
    if lease.include_vat:
        vat_amount = amount * 0.16  # Kenya VAT rate 16%
        description += " (incl. VAT)"
    
    invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": tenant.linked_customer,
        "due_date": get_first_day(add_days(nowdate(), 3)),
        "items": [{
            "item_code": property.linked_item,
            "qty": 1,
            "rate": amount,
            "amount": amount,
            "description": description,
            "taxes": [{
                "charge_type": "Actual",
                "account_head": "VAT 16% - KRA",
                "description": "Value Added Tax",
                "tax_amount": vat_amount
            }] if lease.include_vat else []
        }],
        "custom_lease": lease.name,
        "taxes_and_charges": "Kenya VAT" if lease.include_vat else ""
    })
    
    try:
        invoice.insert(ignore_permissions=True)
        invoice.submit()
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(f"Failed to create rent invoice for lease {lease.name}: {str(e)}")

def enqueue_scheduled_tasks():
    """Enqueue all scheduled tasks"""
    enqueue("property_rent_management.scheduler.send_rent_reminders", queue='long')
    enqueue("property_rent_management.scheduler.generate_monthly_rent_invoices", queue='long')

# Hook to run daily
def daily():
    send_rent_reminders()

# Hook to run monthly on 1st day
def monthly():
    if datetime.now().day == 1:
        generate_monthly_rent_invoices()