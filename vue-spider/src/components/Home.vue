<template>
    <div id="home">
        <!-- 面包屑 -->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item>首页</el-breadcrumb-item>
        </el-breadcrumb>

        <el-row>
            <el-col :span="24">
                <!-- 表单 -->
                <el-form inline :model="query" label-position="right" label-width="100px" class="query-form">
                    <el-form-item label="岗位关键词" prop="searchKeyWords">
                        <el-select v-model="query.id" placeholder="请选择" @change="parentChange()">
                            <el-option
                                v-for="item in selfPList"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                            </el-option>
                            <!-- 全部，DATA， | 全部，数据分析，前端 -->
                        </el-select>

                        <el-select v-model="query.name" filterable placeholder="请选择" @change="subChange()">
                            <el-option
                            v-for="item in selfSubList"
                            :key="item.id"
                            :label="item.name"
                            :value="item.name">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <!-- <el-form-item>
                        <el-button type="primary" @click="searchData()">查询</el-button>
                    </el-form-item> -->
                </el-form>
            </el-col>
        </el-row>

        <el-row :gutter="10">
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                <el-card class="box-card" shadow="never">
                    <sw-cloudChart 
                        class="home-cloud" id="home-cloud"
                        :searchWords="query.name"
                        height="300px" width="100%"></sw-cloudChart>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                <el-card class="box-card" shadow="never">
                    <sw-mapChart 
                        class="home-map" id="home-map" 
                        :searchWords="query.name"
                        height="300px" width="100%"></sw-mapChart>
                </el-card>
            </el-col>
        </el-row>
        <el-row :gutter="10">
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                <el-card class="box-card" shadow="never">
                    <sw-pieChart 
                        class="work-pie" id="work-pie"
                        :data="otherinfo.work"
                        height="300px" width="100%" chartTitle="工作年限要求"></sw-pieChart>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                <el-card class="box-card" shadow="never">
                    <sw-pieChart 
                        class="salary-pie" id="salary-pie"
                        :data="otherinfo.salary"
                        height="300px" width="100%" chartTitle="薪水分布"></sw-pieChart>
                </el-card>
            </el-col>
        </el-row>
        <el-row :gutter="10">
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                <el-card class="box-card" shadow="never">
                    <sw-pieChart 
                        class="education-pie" id="education-pie"
                        :data="otherinfo.education"
                        height="300px" width="100%" chartTitle="学历要求"></sw-pieChart>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import VueEvent from '../model/vueEvent.js'
// var echarts = require('echarts');
import MapChart from './echarts/mapChart'
import cloudChart from './echarts/wordCloudChart'
import pieChart from './echarts/pieChart'

export default {
    data() {
        return {
            msg: 'Lance',
            query:{
                id: 1,
                name: '数据分析师'
            },
            plist: [],
            otherinfo: {}
        }
    },
    mounted() {
        VueEvent.$on("getPlist", () => {
            this.plist = this.$store.state.plist
            console.log(this.plist)
            this.searchData()
        })
        if (this.$store.state.plist) {
            this.plist = this.$store.state.plist
            this.searchData()
        }
    },
    methods: {
        parentChange() {
            console.log(this.query.id)
            this.query.name = this.selfSubList.length > 0 ? this.selfSubList[0].name : ''
        },
        subChange() {
            console.log(this.query.name)
        },
        searchData() {
            const params = {
                searchWords: this.query.name
            }
            this.$http.get(
                'http://lance.natapp1.cc/otherInfo', 
                {params}
                ).then(res => {
                console.log("requestData请求到的数据：", res.body)
                if (res.body.status === 200) {
                    this.otherinfo = res.body.datas
                }
            }, err => {
                console.log(err)
            })
        }
    },
    watch: {
        // 监听对象及对应值的变化
        query: {
            handler(val) {
                this.searchData()
            },
            deep: true
        }
    },
    computed: {
        selfPList() {
            return this.plist.map(item => {
                return {
                    id: item.id,
                    name: item.name,
                    pid: item.pid
                }
            })
        },
        selfSubList() {
            let pList = this.plist.filter(item => item.id === this.query.id)
            console.log(pList)
            return pList.length > 0 ? pList[0].subList : []
        }
    },
    components: {
        'sw-mapChart': MapChart,
        'sw-cloudChart': cloudChart,
        'sw-pieChart': pieChart
    }
}
</script>

<style lang="scss">
.text {
    font-size: 14px;
}

.item {
    padding: 18px 0;
}

.box-card {
    // width: 480px;
    // position: relative;
}

.el-row {
    margin-bottom: 20px;
    &:last-child {
        margin-bottom: 0;
    }
}

.el-col {
    border-radius: 4px;
}
.bg-purple-dark {
    background: #99a9bf;
}
.bg-purple {
    background: #d3dce6;
}
.bg-purple-light {
    background: #e5e9f2;
}
.grid-content {
    border-radius: 4px;
    min-height: 36px;
}
</style>
