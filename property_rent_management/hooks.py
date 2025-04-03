app_name = "property_rent_management"
app_title = "Property Rent Management"
app_publisher = "Your Name"
app_description = "Property Management System for ERPNext with Kenya Market Support"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "your@email.com"
app_license = "MIT"

# Frontend Assets
app_include_js = ["/assets/property_rent_management.bundle.js"]
app_include_css = ["/assets/property_rent_management.bundle.css"]

# Dependencies
app_version = "1.0.0"
required_apps = ["frappe"]

# Development Settings
vite_config_path = "property_rent_management/vite.config.js"
dev_server = {
    "host": "localhost",
    "port": 8080,
    "hot": True
}

# Website Routes
website_route_rules = [
    {"from_route": "/property-rent-management", "to_route": "property_rent_management"}
]

# Fixtures
fixtures = [
    {
        "doctype": "Print Format",
        "filters": [["module", "in", ["Property Rent Management"]]]
    }
]
