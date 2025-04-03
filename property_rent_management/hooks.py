app_name = "property_rent_management"
app_title = "Property Rent Management"
app_publisher = "Your Name"
app_description = "Property Management System for ERPNext with Kenya Market Support"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "your@email.com"
app_license = "MIT"

app_include_js = "/assets/property_rent_management.bundle.js"
app_include_css = "/assets/property_rent_management.bundle.css"

website_route_rules = [
    {"from_route": "/property-rent-management", "to_route": "property_rent_management"}
]

fixtures = [
    {
        "doctype": "Print Format",
        "filters": [["module", "in", ["Property Rent Management"]]]
    }
]
