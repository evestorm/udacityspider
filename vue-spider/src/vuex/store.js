// import Vue from 'vue'
// import Vuex from 'vuex'
Vue.use(Vuex)

/*1.state在vuex中用于存储数据*/
const state = {
    plist: [] // 侧边栏分类
}

const mutations = {
    // 存储plist
    storePlist(state, plist) {
        state.plist = plist
    }
}

const store = new Vuex.Store({
    state,
    mutations
})

export default store