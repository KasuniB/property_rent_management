const esbuild = require('esbuild');

// Test build configuration
async function testBuild() {
  try {
    // Test JS build
    await esbuild.build({
      entryPoints: ['public/js/property_rent_management.js'],
      bundle: true,
      minify: true,
      sourcemap: true,
      outfile: 'public/js/property_rent_management.min.js',
      platform: 'browser',
      target: ['es2015'],
      format: 'iife'
    });

    // Test CSS build
    await esbuild.build({
      entryPoints: ['public/css/property_rent_management.css'],
      bundle: true,
      minify: true,
      sourcemap: true,
      outfile: 'public/css/property_rent_management.min.css'
    });

    console.log('✅ Build test successful');
  } catch (error) {
    console.error('❌ Build test failed:', error);
    process.exit(1);
  }
}

testBuild();