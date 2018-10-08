var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    context: __dirname,
    entry: {
        'index': './assets/dev/default/index.js',
        'dashboard/index': './assets/dev/dashboard/js/index.js'
    },
    output: {
        path: path.resolve("./assets/bundles"),
        filename: "[name].js",
        publicPath: '/static/bundles/'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /\.scss$/,
                use: ['style-loader', 'css-loader', 'sass-loader']
            },
            {
                test: /\.(png|jpg|gif)$/,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            limit: 5000
                        }
                    }
                ]
            }
        ]
    },

    plugins: [
        new BundleTracker(
            { filename: './webpack-stats.json' }
        ),
        new MiniCssExtractPlugin()
    ]
}