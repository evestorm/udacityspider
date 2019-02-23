<template>
    <!--来源： https://blog.csdn.net/weixin_38641550/article/details/82149696 -->
    <div :class="className" :id="id" :style="{height:height, width:width}" ref="myEchart"></div>
</template>
<script>
// import echarts from 'echarts'
// import echartsWordcloud from 'echarts-wordcloud'

export default {
    data() {
        return {
            chart: null,
            options: {
                title: {
                    text: '高频词',
                    x: 'center',
                },
                tooltip: {
                    show: true
                },
                series: [{
                    name: '高频词',
                    type: 'wordCloud',
                    size: ['80%', '80%'],
                    textRotation: [0, 45, 90, -45],
                    textPadding: 0,
                    autoSize: {
                        enable: true,
                        minSize: 14
                    },
                    data: [
                    ],
                    textStyle: {
                        normal: {
                            fontFamily: '微软雅黑',
                            color: function () {
                                // return 'rgb(' + [
                                //     Math.round(Math.random() * 31),
                                //     Math.round(Math.random() * 180),
                                //     Math.round(Math.random() * 226)
                                // ].join(',') + ')';
                                return 'rgb(31,160,246)'
                            }
                        }
                    },
                }]
            },
        }
    },
    beforeDestroy() {
        if (!this.chart) {
            return
        }
        this.chart.dispose();
        this.chart = null;
    },
    mounted() {
        this.initChart();
        this.requestData();
    },
    methods: {
        requestData() {
            const params = {
                searchWords: this.searchWords,
            }
            this.$http.get(
                'http://lance.natapp1.cc/jieba', 
                {params}
                ).then(res => {
                console.log("requestData请求到的数据：", res.body)
                if (res.body.status === 200) {
                    this.options.series[0].data = res.body.datas.map(item => {
                        return {
                            name: item.word,
                            value: Math.ceil(item.weight)
                        }
                    })
                    this.chart.setOption(this.options)
                }
            }, err => {
                console.log(err)
            })
        },
        initChart() {
            // 基于准备好的dom，初始化echarts实例
            this.chart = echarts.init(document.getElementById(this.id));
            // 绘制图表
            let option = this.options
            // 为echarts对象加载数据
            this.chart.setOption(option)
            window.addEventListener("resize", () => { this.chart.resize()}, false);
        }
    },
    watch: {
        searchWords(val) {
            console.log(val)
            this.requestData()
        }
    },
    props: {
        className: {
            type: String,
            default: 'chart'
        },
        id: {
            type: String,
            default: 'chart'
        },
        width: {
            type: String,
            default: '300px'
        },
        height: {
            type: String,
            default: '300px'
        },
        searchWords: {
            type: String,
            default: '数据分析师'
        }
    }
}
</script>
<style>

</style>