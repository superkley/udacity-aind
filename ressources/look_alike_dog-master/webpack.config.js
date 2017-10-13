const path = require('path');

module.exports = {
    entry: [
        './frontend/index.js'
    ],
    output: {
        path: path.resolve('backend/static/build'),
        publicPath: '/',
        filename: 'bundle.js'
    },
    module: {
        loaders: [{
            exclude: /node_modules/,
            loader: 'babel-loader',
            query: {
                presets: ['react', 'es2015', 'stage-1']
            }
        }
        ]
    },
    resolve: {
        extensions: ['.js', '.jsx']
    }
}
