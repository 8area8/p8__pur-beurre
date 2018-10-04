var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: {
        'index': './assets/dev/default/js/index.js',
        'dashboard/index': './assets/dev/dashboard/js/index.js'
    },
    output: {
        path: path.resolve("./assets/bundles"),
        filename: "[name].js"
    },

    plugins: [
        new BundleTracker({ filename: './webpack-stats.json' })
    ]
}