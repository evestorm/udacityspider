### 分类页面路由：/list/data/1
```js
// plist结构：
plist = [
    {id: 1, name: 'DATA', pid: 0, subList: [
        {
            id: 5
            name: "数据分析师"
            pid: 1
        }
    ]}
]
```
#### 路由变化
- 侧边栏点击【两个参数，一二级index】：传递二维数组索引 [0, 0] 拿到plist中的plist[0]['subList'][0]
- _options_面包屑点击（一级分类点击）【一个参数，一级index】：跳转到当前一级分类下的第一个子分类 plist[0]['subList'][0]
- 直接修改路由：/list/data/1 表示一级分类下DATA下的第一个子分类“数据分析师” ——>需要转化为 plist[0]['subList'][0]
```js
// 面包屑展示：
breadList: [
    {
        path: 0,
        name: 'DATA'
    },
    {
        path: 0,
        name: '数据分析师'
    }
],
```

```js
插件
webpack-bundle-analyzer ——> 查看打包详细分布，优化打包体积
babel-polyfill ——> es6转es5

Webpack 出现 Invalid Host header 错误 ,可将 webpack-dev-server  disableHostCheck 设置为true p.s. 在package.json中的 dev 中设置

为了提速把vue,vuex等插件全部用cdn引入的方式放进了index.html，还需要同步在webpack.config.js中的 externals 里添加对应的包名，让webpack不打包这些插件

懒加载路由（见router/index.js文件，注意要把 .babelrc 中原来的 stage-3 改为 stage-2）
```