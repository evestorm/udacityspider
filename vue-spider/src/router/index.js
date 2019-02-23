// import Vue from 'vue'
// import VueRouter from 'vue-router'

Vue.use(VueRouter)

// import Home from '../components/Home.vue'
// import List from '../components/List.vue'

function loadView(view) {
    return () => import(`../components/${view}.vue`)
}

const router = new VueRouter({
    routes: [
        { path: '/home', component: loadView('Home') },
        { path: '/list/:type/:index', component: loadView('List') },
        { path: '*', redirect: '/home' }
    ]
})

export default router