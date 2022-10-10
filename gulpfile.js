////////////////////////////////
// Setup
////////////////////////////////

// Gulp and package
const { src, dest, parallel, series, watch } = require('gulp');
const pjson = require('./package.json');

// Plugins
const gulpif = require('gulp-if');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var rollup = require('@rollup/stream');
const browserSync = require('browser-sync').create();

// tailwindcss
const autoprefixer = require('autoprefixer');
const tailwindcss = require('tailwindcss');
const purgecss = require('gulp-purgecss');
const postcss = require('gulp-postcss');

const sourcemaps = require('gulp-sourcemaps');
const cssnano = require('cssnano');
const imagemin = require('gulp-imagemin');
const pixrem = require('pixrem');
const plumber = require('gulp-plumber');
const reload = browserSync.reload;
const rename = require('gulp-rename');
const sass = require('gulp-sass')(require('sass'));
const spawn = require('child_process').spawn;
const uglify = require('gulp-uglify-es').default;

// *Optional* Depends on what JS features you want vs what browsers you need to support
// *Not needed* for basic ES6 module import syntax support
var babel = require('@rollup/plugin-babel');

// Add support for require() syntax
var commonjs = require('@rollup/plugin-commonjs');

// Add support for importing from node_modules folder like import x from 'module-name'
var nodeResolve = require('@rollup/plugin-node-resolve');

// Cache needs to be initialized outside of the Gulp task
var cache;

const TailwindExtractor = (content) => {
  return content.match(/[A-z0-9-:\/]+/g) || [];
};

// Relative paths function
function pathsConfig() {
  this.app = `./${pjson.name}`;
  const vendorsRoot = 'node_modules';

  return {
    nodeModules: `${vendorsRoot}`,
    vendorsJs: [
      `${vendorsRoot}/@popperjs/core/dist/umd/popper.js`,
      `${vendorsRoot}/bootstrap/dist/js/bootstrap.js`
    ],
    app: this.app,
    templates: `${this.app}/templates`,
    css: `${this.app}/static/css`,
    sass: `${this.app}/static/sass`,
    fonts: `${this.app}/static/fonts`,
    images: `${this.app}/static/images`,
    js: `${this.app}/static/js`,
    tailwind: `./tailwind.config.js`
  };
}

var paths = pathsConfig();

////////////////////////////////
// Tasks
////////////////////////////////

// Styles autoprefixing and minification
function styles() {
  var processCss = [
    tailwindcss(paths.tailwind),
    autoprefixer(), // adds vendor prefixes
    pixrem() // add fallbacks for rem units
  ];

  var minifyCss = [
    cssnano({ preset: 'default' }) // minify result
  ];

  return (
    src(`${paths.sass}/project.scss`)
      .pipe(
        sass({
          includePaths: [paths.nodeModules, paths.sass]
        }).on('error', sass.logError)
      )
      .pipe(plumber()) // Checks for errors
      .pipe(
        gulpif(
          process.env.NODE_ENV === 'production',
          purgecss({
            content: [
              `${paths.templates}/**/*.html`,
              `${paths.sass}/**/*.scss`,
              `${paths.js}/**/*.js`
            ],
            extractors: [
              {
                extractor: TailwindExtractor,
                extensions: ['html', 'js', 'scss']
              }
            ]
          })
        )
      )
      .pipe(dest(paths.css))
      .pipe(postcss(processCss))
      .pipe(rename({ suffix: '.min' }))
      .pipe(postcss(minifyCss)) // Minifies the result
      .pipe(dest(paths.css))
  );
}

// ref - https://stackoverflow.com/a/59786169/5123867
// Javascript minification
function scripts() {
  return (
    rollup({
      // Point to the entry file
      input: `${paths.js}/project.js`,

      // Apply plugins
      plugins: [babel, commonjs, nodeResolve],

      // Use cache for better performance
      cache: cache,

      // Note: these options are placed at the root level in older versions of Rollup
      output: {
        // Output bundle is intended for use in browsers
        // (iife = "Immediately Invoked Function Expression")
        format: 'iife',

        // Show source code when debugging in browser
        sourcemap: true
      }
    })
      .on('bundle', function (bundle) {
        // Update cache data after every bundle is created
        cache = bundle;
      })
      // Name of the output file.
      .pipe(source('bundle.js'))
      .pipe(buffer())
      .pipe(plumber()) // Checks for errors
      .pipe(gulpif(process.env.NODE_ENV === 'production', uglify())) // Minifies the js
      // The use of sourcemaps here might not be necessary,
      // Gulp 4 has some native sourcemap support built in
      .pipe(sourcemaps.init({ loadMaps: true }))
      .pipe(sourcemaps.write('.'))
      .pipe(rename({ suffix: '.min' }))
      // Where to send the output file
      .pipe(dest(paths.js))
  );
  // return src(`${paths.js}/project.js`)
  //   .pipe(plumber()) // Checks for errors
  //   .pipe(uglify()) // Minifies the js
  //   .pipe(rename({ suffix: '.min' }))
  //   .pipe(dest(paths.js))
}
// Vendor Javascript minification
/* No longer required */
// function vendorScripts() {
//   return src(paths.vendorsJs)
//     .pipe(concat('vendors.js'))
//     .pipe(dest(paths.js))
//     .pipe(plumber()) // Checks for errors
//     .pipe(uglify()) // Minifies the js
//     .pipe(rename({ suffix: '.min' }))
//     .pipe(dest(paths.js))
// }

// Image compression
function imgCompression() {
  return src(`${paths.images}/*`)
    .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
    .pipe(dest(paths.images));
}
// Run django server
function runServer(cb) {
  var cmd = spawn('python', ['manage.py', 'runserver'], { stdio: 'inherit' });
  cmd.on('close', function (code) {
    console.log('runServer exited with code ' + code);
    cb(code);
  });
}

// Browser sync server for live reload
function initBrowserSync() {
  browserSync.init([`${paths.css}/*.css`, `${paths.js}/*.js`, `${paths.templates}/**/*.html`], {
    // https://www.browsersync.io/docs/options/#option-proxy
    proxy: 'localhost:8000',
    open: false
  });
}

// Watch
function watchPaths() {
  watch([`${paths.sass}/**/*.scss`, `${paths.templates}/**/*.html`], styles).on('change', reload);
  watch([`${paths.js}/**/*.js`, `!${paths.js}/*.min.js`], scripts).on('change', reload);
}

// Generate all assets
const generateAssets = parallel(
  styles,
  scripts,
  // vendorScripts,
  imgCompression
);

// Set up dev environment
const dev = parallel(runServer, initBrowserSync, watchPaths);

exports.default = series(generateAssets, dev);
exports['generate-assets'] = generateAssets;
exports['dev'] = dev;
