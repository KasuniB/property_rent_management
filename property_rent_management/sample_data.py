import frappe
from frappe.utils import nowdate, add_months

def create_sample_data():
    # Create sample properties
    properties = [
        {
            "property_name": "Downtown Apartment",
            "property_type": "Apartment",
            "address": "123 Main St, Downtown",
            "monthly_rent": 1500,
            "availability_status": "Available"
        },
        {
            "property_name": "Suburban House",
            "property_type": "House",
            "address": "456 Oak Ave, Suburbia",
            "monthly_rent": 2200,
            "availability_status": "Available"
        },
        {
            "property_name": "Office Space A",
            "property_type": "Office",
            "address": "789 Business Blvd, Downtown",
            "monthly_rent": 3500,
            "availability_status": "Leased"
        }
    ]

    for prop in properties:
        property = frappe.get_doc({
            "doctype": "Property",
            **prop
        }).insert()
        if prop["availability_status"] == "Leased":
            property.availability_status = "Available"
            property.save()

    # Create sample tenants
    tenants = [
        {
            "full_name": "John Smith",
            "contact_number": "555-123-4567",
            "email": "john.smith@example.com"
        },
        {
            "full_name": "Sarah Johnson",
            "contact_number": "555-987-6543",
            "email": "sarah.j@example.com"
        }
    ]

    for tenant_data in tenants:
        tenant = frappe.get_doc({
            "doctype": "Tenant",
            **tenant_data
        }).insert()

    # Create active lease
    lease = frappe.get_doc({
        "doctype": "Lease",
        "property": "Office Space A",
        "tenant": "John Smith",
        "start_date": add_months(nowdate(), -2),
        "end_date": add_months(nowdate(), 10),
        "rent_amount": 3500,
        "lease_status": "Active"
    }).insert()
    lease.submit()

    # Create rent payment
    payment = frappe.get_doc({
        "doctype": "Rent Payment",
        "linked_lease": lease.name,
        "payment_date": nowdate(),
        "amount_paid": 3500,
        "payment_method": "Online Transfer"
    }).insert()
    payment.submit()

    # Create maintenance request
    maintenance = frappe.get_doc({
        "doctype": "Maintenance Request",
        "property": "Office Space A",
        "reported_by": "John Smith",
        "issue_type": "Electrical",
        "description": "Lights in hallway not working",
        "priority": "High"
    }).insert()
    maintenance.submit()

    print("""
    Sample data created successfully:
    - 3 properties (1 leased, 2 available)
    - 2 tenants
    - 1 active lease with payment
    - 1 maintenance request
    """)
