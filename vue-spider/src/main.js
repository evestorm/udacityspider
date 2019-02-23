// import ElementUI from 'element-ui' //新添加
// import 'element-ui/lib/theme-chalk/index.css' //新添加，避免后期打包样式不同，要放在import App from './App';之前
import 'element-ui/lib/theme-chalk/reset.css'
import './styles/index.scss'

// import Vue from 'vue'
import App from './App.vue'
// import VueResource from 'vue-resource'
Vue.use(VueResource)

import router from './router/index'

new Vue({
  el: '#app',
  render: h => h(App),
  router
})
