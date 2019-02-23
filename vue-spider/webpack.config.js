var path = require('path')
var webpack = require('webpack')

const {
  BundleAnalyzerPlugin
} = require('webpack-bundle-analyzer');

const HtmlWebpackPlugin = require('html-webpack-plugin')


module.exports = {
  entry: './src/main.js',
  // 关于webpack的path和publicPath https://www.cnblogs.com/gaomingchao/p/6911762.html
  output: {
    path: path.resolve(__dirname, 'dist'), // 所有输出文件的目标路径;
    publicPath: '', // 输出解析文件的目录，url 相对于 HTML 页面
    filename: '[name].bundle.js',
    chunkFilename: '[id].chunk.js',
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader'
        ],
      },
      {
        test: /\.scss$/,
        use: [
          'vue-style-loader',
          'css-loader',
          'sass-loader'
        ],
      },
      {
        test: /\.sass$/,
        use: [
          'vue-style-loader',
          'css-loader',
          'sass-loader?indentedSyntax'
        ],
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
            // Since sass-loader (weirdly) has SCSS as its default parse mode, we map
            // the "scss" and "sass" values for the lang attribute to the right configs here.
            // other preprocessors should work out of the box, no loader config like this necessary.
            'scss': [
              'vue-style-loader',
              'css-loader',
              'sass-loader'
            ],
            'sass': [
              'vue-style-loader',
              'css-loader',
              'sass-loader?indentedSyntax'
            ]
          }
          // other vue-loader options go here
        }
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]?[hash]'
        }
      },
      {
        test: /\.(ttf|eot|svg|woff|woff2)$/,
        use: 'url-loader'
      }, // 处理 字体文件的 loader
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    },
    extensions: ['*', '.js', '.vue', '.json']
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true,
    overlay: true
  },
  performance: {
    hints: false
  },
  devtool: '#eval-source-map',
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerPort: 8768
    }),
    new HtmlWebpackPlugin({
      template: path.resolve(__dirname, './index.html')
    })
  ],
  externals: { // 让webpack不打包下面列出来的包，因为改为了cdn引入
    'vue': 'Vue',
    'vue-router': 'VueRouter',
    'vuex': 'Vuex',
    'element-ui': 'ELEMENT',
    "echarts": "echarts",
    "vue-resource": 'VueResource'
  }
}

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '#source-map'
  // module.exports.output = {
  //   path: path.resolve(__dirname, './dist'),
  //   publicPath: '/dist/',
  //   filename: '[name].[hash].js',
  // },
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false,
        drop_debugger: true,
        drop_console: true
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}
