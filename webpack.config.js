var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: './django_apps/djangowebpack/static/js/index.js',
    output: {
        path: path.resolve('./django_apps/djangowebpack/static/webpack_bundles/'),
        filename: "[name].js"
    },

    plugins: [
        new BundleTracker({ filename: './webpack-stats.json' })
    ]
}