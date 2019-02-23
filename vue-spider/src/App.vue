<template>
  <el-container class="wrapper">
    <!-- 头部 -->
    <el-header
      height="80px"
      :style="{ 'background-color': primaryColor }"
      class="header">
      <img
        src="https://cn.udacity.com/assets/iridium/images/core/header/udacity-wordmark-light-cn.svg"
        alt="udacity-logo"
        class="header-logo"
        height="60px"
        >
    </el-header>
    <!-- 主体 -->
    <el-container>
      <!-- 侧边栏 -->
      <sw-aside :defaultActive="defaultActive"></sw-aside>
      <!-- 右边内容 -->
      <el-main class="content">
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import Aside from './components/subComponents/Aside'
import VueEvent from './model/vueEvent.js'

import store from './vuex/store'

export default {
  name: 'app',
  data () {
    return {
      primaryColor: '#409eff',
      defaultActive: '/home' // 默认侧边栏高亮
    }
  },
  mounted() {
    // 设置当前导航栏分类高亮
    VueEvent.$on("get-default-active", data => {
      console.log("APP改了", data)
      this.$nextTick(function() {
        this.defaultActive = data
      })
    })
  },
  methods: {
    toggleAside() {
      this.isHide = !this.isHide;
    }
  },
  watch: {
  },
  components: {
    'sw-aside': Aside,
  },
  store
}
</script>

<style lang="scss">
.el-container {
  flex-basis: 100%;

  .header-operations li {
    &.active {
      font-weight: 600;
    }
  }

  .el-menu-item {
    a {
      color: #000;
      display: block;
    }
    &.is-active a {
      color: #409EFF;
    }

  }
}
</style>
