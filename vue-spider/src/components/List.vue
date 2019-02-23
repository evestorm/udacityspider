<template>
    <div id="List">
        <!-- 面包屑 -->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item>分类</el-breadcrumb-item>
            <el-breadcrumb-item v-for="(item, index) in breadList" :key="index">{{item.name}}</el-breadcrumb-item>
            <el-button @click="exportFunc()" style="float: right; padding: 3px 0" type="text">下载excel</el-button>
        </el-breadcrumb>
        <!-- 表单 -->
        <el-form inline :model="query" label-position="right" label-width="80px" class="query-form">
            <el-form-item label="岗位名称" prop="pname">
                <el-input v-model="query.pname" placeholder="请输入岗位名称"></el-input>
            </el-form-item>
            <el-form-item label="日期" prop="ctiem">
            <el-date-picker
                v-model="query.ctime"
                type="daterange"
                start-placeholder="开始日期"
                range-separator="至"
                end-placeholder="结束日期"
                value-format="yyyy-MM-dd">
            </el-date-picker>
            </el-form-item>
            <el-form-item>
            <el-button type="primary" @click="searchData()">搜索</el-button>
            </el-form-item>
        </el-form>

        <!-- 表格数据 -->
        <el-table :data="list" class="table" id="out-table" stripe border>
            <!-- 展开后的所有数据 -->
            <el-table-column type="expand">
                <template slot-scope="props">
                    <el-form label-position="left" inline class="demo-table-expand">
                        <el-form-item v-for="(value, key) in tableLabel" :key="key"
                            :label="value"
                            >
                            <span>{{ props.row[key] }}</span>
                        </el-form-item>
                    </el-form>
                </template>
            </el-table-column>
            <!-- 重要的数据：利用computed对tableLabel进行了过滤 -->
            <el-table-column v-for="(value, key) in importantTableLabel" :key="key"
                :label="value"
                :prop="key"
                >
            </el-table-column>

            <!-- <el-table-column v-for="(value, key) in tableLabel" :key="key" 
                :prop="key" 
                :label="value"
                width="120"
                :sortable="key=='createTime' || key=='positionId'"></el-table-column> -->
            <el-table-column label="操作" width="80" fixed="right">
                <template slot-scope="props">
                    <el-button size="mini">
                        <a :href="`https://www.lagou.com/jobs/${props.row['positionId']}.html`" target="_blank">详情</a>
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <sw-pager 
            :total="allCount" 
            :display="20" 
            :currentPage="currentPage"
            @change-curPage="changeCurPage"></sw-pager>
            <!-- vue 子组件通知父组件刷新数据
            链接：https://segmentfault.com/q/1010000010137411 -->
    </div>
        
</template>

<script>
import StandardPagination from './pagination/StandardPagination'
import VueEvent from '../model/vueEvent.js'

// import FileSaver from 'file-saver'; 不需要，在服务端就保存好了
// import XLSX from 'xlsx'; 同上

export default {
    data() {
        const tableLabel = {
            positionId: '岗位ID',
            positionName: '岗位名称',
            city: '城市',
            workYear: '工作经验',
            education: '教育程度',
            salary: '薪资',
            companyShortName: '公司简称',
            jobNature: '工作性质',
            createTime: '发布时间',

            companySize: '公司规模',
            industryField: '工业领域',
            positionAdvantage: '岗位优势',
            financeStage: '融资阶段',
            positionLables: '岗位标签',
            companyLabelList: '公司标签',
            companyFullName: '公司全称',
            isSchoolJob: '是否实习',
            skillLables: '技能标签'
        }
        return {
            breadList: [
                {
                    path: 0, // plist中一级分类索引
                    name: 'DATA'
                },
                {
                    path: 0, // plist中二级分类索引
                    name: '数据分析师'
                }
            ],
            defaultActive: '1', // 默认当前分类的高亮索引值
            cid: '4', // 默认分类 4：前端开发工程师
            tableLabel, // 表格标题
            query: { // 查询条件
                pname: '',
                ctime: []
            },
            currentPage: 1,
            allCount: 0, // 当前查询数据总条数
            plist: [], // 职位分类
            list: [], // 职位数据
            downloadURL: '' // excel下载地址
        }
    },
    mounted() {
        console.log("mounted:", this.$route)
        console.log(this.$store.state.plist)
        if (this.$store.state.plist.length > 0) {
            this.plist = this.$store.state.plist
            this.cid = this.plist[0].subList[0].id
            this.checkRouteAndGetData(this.$route.params)
        }
        // 获取侧边栏数据
        VueEvent.$on("getPlist", () => {
            this.plist = this.$store.state.plist
            this.cid = this.plist[0].subList[0].id
            this.checkRouteAndGetData(this.$route.params)
        })

        VueEvent.$on('change-menu', (index, index2) => {
            this.resetSearchItem()
            this.$router.push({ path: `/list/${this.plist[index].name.toLowerCase()}/${index2+1}` })
        })
    },
    methods: {
        // 请求职位列表数据
        requestData() {
            let { pname, ctime } = this.query
            const params = {
                page: this.currentPage,
                cid: this.cid,
                pname: pname,
                stime: !ctime ? '' : ctime[0],
                etime: !ctime ? '' : ctime[1]
            }
            console.log("requestData的params：", params)
            this.$http.get(
                'http://lance.natapp1.cc/jobs/list',
                {params}
                ).then(res => {
                console.log("requestData请求到的数据：", res.body)
                if (res.body.status === 200) {
                    this.allCount = res.body.allCount
                    this.downloadURL = res.body.downloadURL
                    this.list = res.body.datas.map((item) => {
                        if (item.createTime) {
                            item.createTime = item.createTime.slice(0, 10)
                        }
                        item.isSchoolJob = item.isSchoolJob == 0 ? '否' : '是'
                        return item
                    });
                } else {
                    this.allCount = 0
                    this.list = []
                }
            }, err => {
                console.log(err)
            })
        },
        // 检查所传路由是否存在，存在则请求路由所指数据
        checkRouteAndGetData(params) {
            // 示例：
            // params: {
            //     type: 'data',
            //     index: 1
            // }
            // 声明一级分类&&二级分类对象
            let cateObj, subCateObj
            // 根据路由参数找出一级分类索引
            let cateObjIndex = this.plist.findIndex( item => item.name.toLowerCase() === params.type.toLowerCase())
            console.log(this.plist)
            if (cateObjIndex > -1) {
                // 根据索引找出一级分类对象
                cateObj = this.plist[cateObjIndex]
                // 找到二级分类对象
                subCateObj = cateObj['subList'][params.index-1]
                // 如果一二级分类都存在，则赋值路由对象breadList && 发起请求
                if (cateObj && subCateObj) {
                    console.log("checkRouteAndGetData：")
                    console.log("   一级分类：", cateObj)
                    console.log("   二级分类：", subCateObj)
                    this.breadList = [
                        {
                            path: cateObjIndex,
                            name: cateObj.name
                        }, {
                            path: params.index-1,
                            name: subCateObj.name
                        }
                    ]
                    this.defaultActive = `/list/${cateObj.name.toLowerCase()}/${params.index}`
                    console.log(this.defaultActive)
                    VueEvent.$emit("get-default-active", this.defaultActive)
                    this.cid = this.plist[cateObjIndex]['subList'][params.index-1].id
                    this.requestData()
                } else {
                    // 没有，则代表路由有误，跳转到默认1-1
                    this.resetSearchItem()
                    this.$router.push({ path: `/list/${this.plist[0].name.toLowerCase()}/${1}` })
                }
            }
        },
        // 点击搜索按钮触发
        searchData() {
            this.currentPage = 1
            this.requestData()
        },
        // 重置搜索栏和当前page
        resetSearchItem() {
            this.query.pname = ''
            this.query.ctime = []
            this.currentPage = 1
        },
        // 点击分页后触发
        changeCurPage(page) {
            this.currentPage = page
            this.requestData()
        },
        // TODO: 导出excel
        // 前端导出方案：https://www.cnblogs.com/tugenhua0707/p/8597050.html
        // 后端导出方案：？
        exportFunc() {
            // 你点击了导出按钮
            let { pname, ctime } = this.query
            console.log(this.cid)
            const params = {
                cid: this.cid,
                pname: pname,
                stime: !ctime ? '' : ctime[0],
                etime: !ctime ? '' : ctime[1]
            }
            console.log("requestData的params：", params)

            // 下载文件方法：https://blog.csdn.net/hani_wen/article/details/81952001
            this.$http.get(
                'http://lance.natapp1.cc/jobs/exportExcel',
                {params}
                ).then(res => {
                console.log("exportFunc请求到的数据：", res.body)
                if (res.body.status === 200) {
                    this.downloadURL = res.body.downloadURL
                    window.location.href = this.downloadURL
                } else {
                    alert("当前导出文件错误，请刷新重试")
                    return
                }
            }, err => {
                console.log(err)
                alert("当前导出文件错误，请刷新重试")
                return
            })
        }
    },
    computed: {
        // 表格中重要的标签【不隐藏的】
        importantTableLabel() {
            let tempObj = {}
            for (const item in this.tableLabel) {
                if (item == 'positionName' || 
                    item == 'city' ||
                    item == 'workYear' ||
                    item == 'education' ||
                    item == 'salary' ||
                    item == 'companyShortName' ||
                    item == 'jobNature' ||
                    item == 'createTime') {
                    tempObj[item] = this.tableLabel[item]
                }
            }
            return tempObj
        }
    },
    watch: {
        // 监视路由
        $route(to, from) {
            console.log(to, from)
            let newParams = to.params
            // 将newParams传递给checkRouteAndGetData，让其处理是否刷新数据
            this.checkRouteAndGetData(newParams)
        }
    },
    components: {
        'sw-pager': StandardPagination
    }
}

// const tableLabelMap = {
//             id: 'ID',
//             companyId: '公司ID',
//             workYear: '工作经验',
//             education: '教育程度',
//             jobNature: '工作性质',
//             positionName: '岗位名称',
//             positionId: '岗位ID',
//             createTime: '发布时间',
//             city: '城市',
//             companyLogo: '公司LOGO',
//             industryField: '工业领域',
//             positionAdvantage: '岗位优势',
//             salary: '薪资',
//             companySize: '公司规模',
//             companyShortName: '公司简称',
//             positionLables: '岗位标签',
//             financeStage: '融资阶段',
//             companyLabelList: '公司标签',
//             longitude: '经度',
//             latitude: '纬度',
//             companyFullName: '公司全称',
//             firstType: '一级分类',
//             secondType: '二级分类',
//             isSchoolJob: '是否实习',
//             thirdType: '三级分类',
//             skillLables: '技能标签',
//             searchKeyWords: '搜索关键词'
//         }
</script>

<style lang="scss">
.demo-table-expand {
    font-size: 0;
}
.demo-table-expand label {
    width: 90px;
    color: #99a9bf;
}
.demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
}
</style>