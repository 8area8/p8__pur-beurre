var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: {'index': './django_apps/djangowebpack/static/default/js/index.js',
        'dashboard_bundles/index': './django_apps/djangowebpack/static/dashboard/js/index.js'
    },
    output: {
        path: path.resolve('./assets/bundles'),
        filename: "[name].js"
    },

    plugins: [
        new BundleTracker({ filename: './webpack-stats.json' })
    ]
}