const esbuild = require('esbuild');
const path = require('path');

// Build JS
esbuild.build({
    entryPoints: ['property_rent_management/public/js/property_rent_management.js'],
    bundle: true,
    minify: true,
    sourcemap: true,
    outfile: 'property_rent_management/public/dist/js/property_rent_management.min.js',
    platform: 'browser',
    target: ['es2015']
}).catch(() => process.exit(1));

// Build CSS
esbuild.build({
    entryPoints: ['property_rent_management/public/css/property_rent_management.css'],
    bundle: true,
    minify: true,
    sourcemap: true,
    outfile: 'property_rent_management/public/dist/css/property_rent_management.min.css'
}).catch(() => process.exit(1));