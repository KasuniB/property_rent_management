const esbuild = require('esbuild');
const path = require('path');

// Build JS
esbuild.build({
    entryPoints: ['public/js/index.js'],
    bundle: true,
    minify: true,
    sourcemap: true,
    outfile: 'public/js/property_rent_management.min.js',
    platform: 'browser',
    target: ['es2015'],
    format: 'iife',
    loader: {
        '.js': 'jsx'
    }
}).catch(() => process.exit(1));

// Build CSS
esbuild.build({
    entryPoints: ['public/css/property_rent_management.css'],
    bundle: true,
    minify: true,
    sourcemap: true,
    outfile: 'public/css/property_rent_management.min.css'
}).catch(() => process.exit(1));