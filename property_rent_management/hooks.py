app_name = "property_rent_management"
app_title = "Property Rent Management"
app_publisher = "Your Name"
app_description = "Property Management System for ERPNext with Kenya Market Support"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "your@email.com"
app_license = "MIT"

# Frontend Assets
# ---------------
app_include_js = [
    "/assets/js/property_rent_management.bundle.js"
]

app_include_css = [
    "/assets/css/property_rent_management.bundle.css"
]

# DocTypes
# --------
doctype_js = {
    "Property": "public/js/doctype/property.js",
    "Tenant": "public/js/doctype/tenant.js",
    "Lease": "public/js/doctype/lease.js",
    "Rent Payment": "public/js/doctype/rent_payment.js"
}

# Website Routes
# -------------
website_route_rules = [
    {"from_route": "/property-rent-management", "to_route": "property_rent_management"}
]

# Fixtures
# --------
fixtures = [
    {
        "doctype": "Print Format",
        "filters": [["module", "in", ["Property Rent Management"]]]
    }
]
