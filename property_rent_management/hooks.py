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
web_include_js = {
    "property_rent_management": [
        "/assets/js/property_rent_management.bundle.js"
    ]
}

web_include_css = {
    "property_rent_management": [
        "/assets/css/property_rent_management.bundle.css"
    ]
}

app_include_js = ["/assets/js/property_rent_management.bundle.js"]
app_include_css = ["/assets/css/property_rent_management.bundle.css"]

# Website Routes
# -------------
website_route_rules = [
    {"from_route": "/property-rent-management", "to_route": "property_rent_management"},
]

# Fixtures
# --------
fixtures = [
    {
        "doctype": "Print Format",
        "filters": [
            [
                "module",
                "in",
                ["Property Rent Management"]
            ]
        ]
    }
]

# DocTypes
# --------
doctype_js = {
    "Property": "public/js/property_rent_management.js",
    "Tenant": "public/js/property_rent_management.js",
    "Lease": "public/js/property_rent_management.js",
    "Rent Payment": "public/js/property_rent_management.js"
}

# Page Assets
# ----------
page_js = {
    "property-rent-management": "public/js/property_rent_management.js"
}
