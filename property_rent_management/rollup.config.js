import resolve from '@rollup/plugin-node-resolve';

export default {
  input: {
    'property_rent_management': 'public/js/property_rent_management.js'
  },
  output: {
    dir: 'public/dist/js',
    format: 'iife',
    name: 'property_rent_management'
  },
  plugins: [
    resolve()
  ]
};