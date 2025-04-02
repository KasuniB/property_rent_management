import frappe

def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 0
    
    # Get system statistics
    context.properties_count = frappe.db.count('Property')
    context.tenants_count = frappe.db.count('Tenant')
    context.active_leases = frappe.db.count('Lease', {'lease_status': 'Active'})
    
    # Get recent activities
    context.recent_leases = frappe.get_list('Lease', 
        fields=['name', 'tenant', 'property', 'start_date', 'end_date'],
        filters={'docstatus': 1},
        order_by='creation desc',
        limit=5
    )
    
    context.recent_payments = frappe.get_list('Rent Payment',
        fields=['name', 'tenant', 'amount', 'payment_date'],
        filters={'docstatus': 1},
        order_by='creation desc',
        limit=5
    )
    
    return context