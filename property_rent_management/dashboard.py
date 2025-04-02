import frappe
from frappe.utils import nowdate, getdate, add_days
from frappe import _

def get_dashboard_data():
    """Fetch all data needed for the property dashboard"""
    return {
        "stats": get_property_stats(),
        "recent_leases": get_recent_leases(),
        "open_requests": get_open_maintenance_requests(),
        "expiring_leases": get_expiring_leases()
    }

def get_property_stats():
    """Get key statistics for properties"""
    return {
        "total_properties": frappe.db.count("Property"),
        "active_leases": frappe.db.count("Lease", {"lease_status": "Active", "docstatus": 1}),
        "overdue_payments": get_overdue_payment_count()
    }

def get_overdue_payment_count():
    """Count overdue rent payments"""
    today = nowdate()
    return frappe.db.count("Rent Payment", {
        "docstatus": 1,
        "payment_date": ["<", today],
        "linked_sales_invoice": ["not in", frappe.db.get_all("Sales Invoice", 
            filters={"status": "Paid"}, pluck="name")]
    })

def get_recent_leases(limit=5):
    """Get recent leases with property and tenant details"""
    leases = frappe.db.get_all("Lease",
        fields=["name", "property", "tenant", "start_date", "end_date", "rent_amount", "lease_status"],
        filters={"docstatus": 1},
        order_by="creation desc",
        limit=limit
    )

    for lease in leases:
        # Add property details
        property = frappe.get_doc("Property", lease.property)
        lease.update({
            "property_name": property.property_name,
            "property_type": property.property_type,
            "property_image": property.image
        })

        # Add tenant details
        tenant = frappe.get_doc("Tenant", lease.tenant)
        lease.update({
            "tenant_name": tenant.full_name,
            "tenant_contact": tenant.contact_number
        })

    return leases

def get_open_maintenance_requests(limit=5):
    """Get open maintenance requests"""
    return frappe.db.get_all("Maintenance Request",
        fields=["name", "property", "issue_type", "description", "priority", "status"],
        filters={"status": ["in", ["Open", "In Progress"]], "docstatus": 1},
        order_by="priority desc, creation desc",
        limit=limit
    )

def get_expiring_leases(days=30):
    """Get leases expiring soon"""
    today = getdate(nowdate())
    end_date = add_days(today, days)

    leases = frappe.db.get_all("Lease",
        fields=["name", "property", "tenant", "end_date"],
        filters={
            "docstatus": 1,
            "lease_status": "Active",
            "end_date": ["between", [today, end_date]]
        },
        order_by="end_date asc"
    )

    for lease in leases:
        lease["days_remaining"] = (getdate(lease.end_date) - today).days
        property = frappe.get_doc("Property", lease.property)
        lease["property_name"] = property.property_name
        tenant = frappe.get_doc("Tenant", lease.tenant)
        lease["tenant_name"] = tenant.full_name

    return leases