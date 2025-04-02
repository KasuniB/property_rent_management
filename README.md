# Property Rent Management

A comprehensive property management system built for ERPNext, with specific features for the Kenyan market.

## Features

- Property management with ERPNext Item integration
- Tenant management with Contact/Customer sync
- Lease agreements with Kenya-compliant terms
- Rent payments with VAT handling (16% Kenya VAT)
- Maintenance request tracking
- Flexible billing cycles (Monthly/Quarterly/Bi-Annual)
- Professional print formats for legal documents

## Installation

```bash
# Get the app
bench get-app property_rent_management https://github.com/[your-username]/property_rent_management

# Install on your site
bench --site [your-site] install-app property_rent_management

# Run migrations
bench --site [your-site] migrate
```

## Configuration

1. Kenya VAT settings are automatically configured on installation
2. Print formats are available immediately
3. Ensure your ERPNext site has basic settings configured:
   - Company
   - Chart of Accounts
   - Tax templates

## Usage

1. Create Properties
2. Add Tenants
3. Generate Lease Agreements
4. Process Rent Payments
5. Handle Maintenance Requests

## License

MIT

## Author

[Your Name]

## Support

For support, please raise an issue on GitHub or contact [your-email]