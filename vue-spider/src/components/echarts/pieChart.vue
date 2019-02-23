<template>
    <!-- 来源：https://gallery.echartsjs.com/editor.html?c=xB1IjqF-Cf -->
    <div :class="className" :id="id" :style="{height:height, width:width}" ref="myEchart"></div>
</template>

<script>
// import echarts from 'echarts'

export default {
    data() {
        return {
            chart: null,
            options: {
                title: {
                    text: this.chartTitle,
                    x:'center'
                },
                legend: {
                    orient: 'vertical',
                    x: 'left',
                    data:[]
                },
                series: [
                    {
                        type:'pie',
                        radius: ['40%', '55%'],
                        label: {
                            normal: {
                                formatter: ' {per|{d}%} ',
                                backgroundColor: '#334455',
                                borderColor: '#aaa',
                                borderWidth: 1,
                                borderRadius: 4,
                                rich: {
                                    b: {
                                        fontSize: 12,
                                        lineHeight: 18
                                    },
                                    per: {
                                        color: '#eee',
                                        padding: [2, 4]
                                    }
                                }
                            },
                            emphasis: {
                                show: true,
                                textStyle: {
                                    fontSize: '16',
                                    fontWeight: 'bold'
                                }
                            }
                        },
                        data:[]
                    }
                ]
            }
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
    },
    methods: {
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
        data(val) {
            this.options.series[0].data = val
            this.options.legend.data = val.map(item=> item.name)
            this.chart.setOption(this.options)
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
        chartTitle: {
            type: String,
            default: ''
        },
        data: {
            type: Array,
            default: function() {
                return []
            }
        }
    }
}
</script>