<template>
    <el-pagination
        class="swpagination"
        background
        @current-change="handleCurrentChange" 
        :current-page.sync="curPage"
        :page-sizes="[display, display*2, display*4, display*6]"
        :page-size="display" 
        layout="total, prev, pager, next, jumper" 
        :total="total">
        <!-- @size-change="handleSizeChange" 
        layout="total, sizes, prev, pager, next, jumper" 每页多少条 -->
    </el-pagination>
</template>

<script>
// TODO: bug1：如果当前某个职位的page为25，切换职位后，页码还会是25，但若此职位没有25页，就会显示无数据
export default {
    data() {
        return {
            curPage: 1
        };
    },
    mounted() {
        // TODO: 当直接修改url地址设置page为其他值时，此处的curPage无法被修改
        this.curPage = this.currentPage
        // console.log(this.curPage)
    },
    methods: {
        // handleSizeChange(val) {
        //     console.log(`每页 ${val} 条`);
        // },
        handleCurrentChange(val) {
            console.log(`当前页: ${val}`);
            this.$emit('change-curPage', val)
        }
    },
    watch: {
        currentPage(val, oldVal) {
            console.log('new: %s, old: %s', val, oldVal)
            this.curPage = val
        }
    },
    props: {
        total: { // 总条数
            type: Number,
            default: 0
        },
        display: {// 每页显示条数
            type: Number,
            default: 20
        },
        currentPage: {// 当前页码
            type: Number,
            default: 1
        }
    }

// vue 封装自定义组件
// 链接：https://www.cnblogs.com/lanchar/p/6894167.html
}
</script>

<style lang="scss" scoped>
.swpagination {
    padding: 20px 0 5px 0;
    text-align: center;
}
</style>
