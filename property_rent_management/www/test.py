import frappe

def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 0
    context.title = "Property Rent Management - Test Page"
    
    # Add some test data to context
    context.properties_count = frappe.db.count('Property')
    context.tenants_count = frappe.db.count('Tenant')
    context.active_leases = frappe.db.count('Lease', {'lease_status': 'Active'})
    
    return context