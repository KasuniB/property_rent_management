const path = require('path');
const esbuild = require('esbuild');

const apps_path = path.resolve(__dirname, '..', '..');
const assets_path = path.resolve(apps_path, 'property_rent_management', 'public');

// Build JS
esbuild.build({
    entryPoints: [path.resolve(assets_path, 'js/property_rent_management.js')],
    bundle: true,
    minify: true,
    sourcemap: true,
    outfile: path.resolve(assets_path, 'js/property_rent_management.min.js'),
    platform: 'browser',
    target: ['es2015'],
    format: 'iife',
    define: {
        'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development')
    }
}).catch(() => process.exit(1));

// Build CSS
esbuild.build({
    entryPoints: [path.resolve(assets_path, 'css/property_rent_management.css')],
    bundle: true,
    minify: true,
    sourcemap: true,
    outfile: path.resolve(assets_path, 'css/property_rent_management.min.css')
}).catch(() => process.exit(1));