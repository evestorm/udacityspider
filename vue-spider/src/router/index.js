// import Vue from 'vue'
// import VueRouter from 'vue-router'

// build后文件过大，要使用 `webpack-bundle-analyzer` 插件插件打包情况
// 如何引入：https://blog.csdn.net/qq_35843477/article/details/84098475
// package.json命令修改：https://blog.csdn.net/qq_19694913/article/details/82628637
Vue.use(VueRouter)

// import Home from '../components/Home.vue'
// import List from '../components/List.vue'

// 改用懒加载路由后，需要把 .babelrc 中原来的 stage-3 改为 stage-2
function loadView(view) {
    return () => import( /* webpackChunkName: "view-[request]" */ `../components/${view}.vue`)
}

const router = new VueRouter({
    routes: [
        { path: '/home', component: loadView('Home') },
        { path: '/list/:type/:index', component: loadView('List') },
        { path: '*', redirect: '/home' }
    ]
})

export default router