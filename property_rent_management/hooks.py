from . import __version__ as app_version

app_name = "property_rent_management"
app_title = "Property Rent Management"
app_publisher = "Your Company"
app_description = "Property and tenant management system integrated with ERPNext"
app_email = "contact@yourcompany.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/property_rent_management/css/property_rent_management.css"
# app_include_js = "/assets/property_rent_management/js/property_rent_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/property_rent_management/css/property_rent_management.css"
# web_include_js = "/assets/property_rent_management/js/property_rent_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "property_rent_management/public/scss/website"

# Document Events
# ---------------
# Hook on document methods and events
doc_events = {
    "Lease": {
        "on_submit": "property_rent_management.lease.create_sales_order",
        "on_cancel": "property_rent_management.lease.cancel_sales_order"
    },
    "Rent Payment": {
        "on_submit": "property_rent_management.rent_payment.create_payment_entry"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "property_rent_management.scheduler.daily"
    ],
    "monthly": [
        "property_rent_management.scheduler.monthly"
    ],
    "all": [
        "property_rent_management.scheduler.enqueue_scheduled_tasks"
    ]
}

# Fixtures
# --------
fixtures = ["Custom Field", "Property", "Tenant", "Lease", "Print Format"]

# Permissions
# -----------
permission_query_conditions = {
    "Lease": "property_rent_management.permissions.get_lease_permission_query",
    "Rent Payment": "property_rent_management.permissions.get_rent_payment_permission_query"
}

# Includes in <head>
# ------------------
app_include_js = "/assets/property_rent_management/js/property_rent_management.min.js"
app_include_css = "/assets/property_rent_management/css/property_rent_management.min.css"

# Website
# -------
website_route_rules = [
    {"from_route": "/property-rent-management", "to_route": "pages/index"},
]

# Testing
# -------
override_whitelisted_methods = {
    "property_rent_management.api.get_property_details": "property_rent_management.tests.test_api.get_property_details"
}

# Post Installation
# -----------------
after_install = "property_rent_management.kenya_vat_setup.after_install"
