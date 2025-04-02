__version__ = '0.0.1'

from frappe import _

def get_data():
    return {
        "fieldname": "property",
        "transactions": [
            {
                "label": _("Rental Operations"),
                "items": ["Lease", "Rent Payment", "Maintenance Request"]
            }
        ]
    }