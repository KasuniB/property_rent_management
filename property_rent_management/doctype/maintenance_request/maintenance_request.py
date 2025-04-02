import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
from erpnext.manufacturing.doctype.work_order.work_order import make_work_order
from erpnext.support.doctype.issue.issue import make_issue

class MaintenanceRequest(Document):
    def validate(self):
        self.validate_property_status()
        self.set_priority_based_response_time()
        
    def validate_property_status(self):
        """Validate property is not under maintenance"""
        property_status = frappe.db.get_value("Property", self.property, "availability_status")
        if property_status == "Under Maintenance":
            frappe.throw("This property is already under maintenance")

    def set_priority_based_response_time(self):
        """Set expected response time based on priority"""
        if self.priority == "Emergency":
            self.expected_response_time = "1 Hour"
        elif self.priority == "High":
            self.expected_response_time = "4 Hours"
        elif self.priority == "Medium":
            self.expected_response_time = "24 Hours"
        else:
            self.expected_response_time = "48 Hours"

    def on_submit(self):
        """Create Issue and Work Order when request is submitted"""
        if not self.linked_issue:
            self.create_issue()
        if self.priority in ["Emergency", "High"] and not self.linked_work_order:
            self.create_work_order()

    def on_update_after_submit(self):
        """Handle status changes"""
        if self.status == "In Progress" and not self.linked_work_order:
            self.create_work_order()
        elif self.status == "Resolved" and self.linked_work_order:
            self.close_work_order()

    def on_cancel(self):
        """Cancel linked Work Order when request is cancelled"""
        if self.linked_work_order:
            wo = frappe.get_doc("Work Order", self.linked_work_order)
            if wo.docstatus == 1:
                wo.cancel()
            self.linked_work_order = None

@frappe.whitelist()
def create_work_order(maintenance_request):
    """Create ERPNext Work Order for maintenance request"""
    mr_doc = frappe.get_doc("Maintenance Request", maintenance_request)
    property_doc = frappe.get_doc("Property", mr_doc.property)

    # Create Work Order
    wo = make_work_order({
        "company": frappe.defaults.get_user_default("company"),
        "production_item": "Maintenance Service",
        "qty": 1,
        "description": mr_doc.description,
        "expected_delivery_date": frappe.utils.add_days(nowdate(), 
            1 if mr_doc.priority in ["Emergency", "High"] else 3),
        "custom_maintenance_request": mr_doc.name,
        "custom_property": mr_doc.property
    })

    try:
        wo.insert(ignore_permissions=True)
        wo.submit()
        mr_doc.linked_work_order = wo.name
        mr_doc.status = "In Progress"
        mr_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return wo.name
    except Exception as e:
        frappe.log_error(f"Failed to create Work Order for Maintenance Request {maintenance_request}: {str(e)}")
        frappe.throw("Failed to create linked Work Order in ERPNext")

@frappe.whitelist()
def create_issue(maintenance_request):
    """Create ERPNext Issue for tracking"""
    mr_doc = frappe.get_doc("Maintenance Request", maintenance_request)
    tenant_doc = frappe.get_doc("Tenant", mr_doc.reported_by)

    # Create Issue
    issue = make_issue({
        "subject": f"Maintenance Request: {mr_doc.issue_type} at {mr_doc.property}",
        "raised_by": tenant_doc.email,
        "description": mr_doc.description,
        "priority": mr_doc.priority,
        "custom_maintenance_request": mr_doc.name,
        "custom_property": mr_doc.property
    })

    try:
        issue.insert(ignore_permissions=True)
        mr_doc.linked_issue = issue.name
        mr_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return issue.name
    except Exception as e:
        frappe.log_error(f"Failed to create Issue for Maintenance Request {maintenance_request}: {str(e)}")
        frappe.throw("Failed to create linked Issue in ERPNext")

@frappe.whitelist()
def close_work_order(maintenance_request):
    """Close linked Work Order when request is resolved"""
    mr_doc = frappe.get_doc("Maintenance Request", maintenance_request)
    if mr_doc.linked_work_order:
        wo = frappe.get_doc("Work Order", mr_doc.linked_work_order)
        if wo.status != "Completed":
            wo.status = "Completed"
            wo.completed_qty = 1
            wo.save(ignore_permissions=True)
            frappe.db.commit()