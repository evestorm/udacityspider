<template>
    <!-- 侧边栏 -->
    <el-aside class="menu" width="200px">
        <el-menu
            :default-active="defaultActive"
            class="el-menu-vertical-demo"
            @open="handleOpen"
            @close="handleClose"
            router>
            <el-menu-item index="/home">
                <span slot="title">首页</span>
            </el-menu-item>
            <el-submenu v-for="(item, index) in plist" :key="index" :index="`/list/${item.name.toLowerCase()}/1`">
                <template slot="title">
                    <span>{{item.name}}</span>
                </template>
                <el-menu-item
                    v-for="(subitem, index2) in item.subList" :key="index2" 
                    :index="`/list/${item.name.toLowerCase()}/${index2+1}`"
                    @click="changeMenu(index, index2)">{{subitem.name}}</el-menu-item>
            </el-submenu>
        </el-menu>
    </el-aside>
</template>

<script>
import VueEvent from '../../model/vueEvent.js'

export default {
    data() {
        return {
            plist: [], // 分类
        }
    },
    mounted() {
        this.requestPList()
    },
    methods: {
        // 侧边栏数据（DATA,AI,WEB）
        requestPList() {
            this.$http.get('http://lance.natapp1.cc/jobs/plist').then( res => {
                console.log("requestPList:", res.body)
                if (res.body.status === 200) {
                    this.plist = this.orderList(res.body.datas)
                    console.log("plist:", this.plist)
                    this.$store.commit("storePlist", this.plist)
                    VueEvent.$emit("getPlist")
                }
            }, err => {
                console.log(err)
            })
        },
        // 改变当前分类的方法
        changeMenu(index, index2) {
            console.log(`当前一级分类索引${index}，当前二级分类索引${index2}`)
            VueEvent.$emit("change-menu", index, index2)
        },
        // 侧边栏展开折叠方法
        handleOpen(key, keyPath) {
            // console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            // console.log(key, keyPath);
        },
        // 整理侧边栏数据
        // 整理前：[{id, name, pid}, ...]
        // 整理后：[{id, name, subList:[id, name, pid]}, ...]
        orderList(plist) {
            let list = plist.filter(item => item.pid === 0)
            for (const item of list) {
                for (const item2 of plist) {
                    if (item.id === item2.pid) {
                        if (!item.subList) {
                            item.subList = []
                        }
                        item.subList.push(item2)
                    }
                }
            }
            // console.log(list)
            return list
        },
    },
    watch: {
    },
    props: {
        defaultActive: {
            type: String,
            default: "/home"
        }
    }
}
</script>