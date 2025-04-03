# Property Rent Management System

A comprehensive property management system for ERPNext with Kenya market support.

## Features

- Property Management
- Tenant Management
- Lease Agreements
- Rent Payments
- Maintenance Requests
- Kenya VAT Support (16%)
- Real-time Dashboard

## Installation

1. Get the app from GitHub:
```bash
bench get-app property_rent_management https://github.com/SajmustafaKe/property_rent_management
```

2. Install on your site:
```bash
bench --site [your-site] install-app property_rent_management
```

3. Build assets:
```bash
bench build --app property_rent_management
```

4. Clear cache and restart:
```bash
bench clear-cache
bench restart
```

## Verification

After installation, verify the app is working by visiting:

1. `/verify` - Quick installation check
2. `/test` - System statistics
3. `/property-rent-management` - Main dashboard

## Support

For issues and feature requests, please create an issue on GitHub.

## License

MIT