<template>
    <div :class="className" :id="id" :style="{height:height, width:width}" ref="myEchart">
    </div>
</template>

<script>
// import echarts from 'echarts'
// 显示地图需要导入下面js
// import china from 'echarts/map/js/china.js' 在index.html中使用了cdn
// import chinaContour from 'echarts/map/js/china-contour.js'
export default {
    data() {
        return {
            chart: null,
            minNums: 0,
            maxNums: 0,
            // 城市地图相关设置：https://www.cnblogs.com/huangxingquan/p/7267494.html
            options: {
                // backgroundColor: '#404A59',
                title: {
                    text: '职位分布',
                    x: 'center',
                    textStyle: {
                        color: '#000'
                    }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function(datas) {
                        let cityName = datas.data.name
                        let nums = datas.data.value[2]
                        return `${cityName} ${nums}`
                    }
                },
                visualMap: {
                    min: this.minNums || 0,//视觉映射组件的最小值
                    max: this.maxNums || 10,//视觉映射组件的最大值
                    calculable: true,
                    inRange: {
                        color: ['#abedd8', '#46cdcf', '#0081c6', '#48466d']
                    },
                    textStyle: {
                        color: '#000'
                    },
                    left: 'left',
                    top: 'bottom',
                    text: ['多', '少'],           // 文本，默认为数值文本
                },
                // legend: {
                //     show: false,
                // },
                geo: {
                    map: 'china',
                    show: true,
                    roam: true,
                    label: {
                        emphasis: {
                            show: false //城市模式下，鼠标移上去不显示省份名称
                        }
                    },
                    itemStyle: {
                        normal: {
                            areaColor: '#eeeeee',
                            borderColor: '#111'
                        },
                        emphasis: {
                            areaColor: '#18bcb4',
                        }
                    }
                },
                series: [{
                    name: '城市',
                    type: 'scatter', // map
                    mapType: 'china',
                    coordinateSystem: 'geo', // 
                    symbolSize: 10,
                    // roam: false,
                    // showLegendSymbol: false,
                    data: [], //当为地图模式即显示省份数据时，数据格式为： [{name: '山东',value: 183 }, {name: '云南',value: 286 }]
                    // 当为散点模式即显示城市数据时，数据格式为： [{name:"厦门",value:[118.1,24.46,183]},{name:"武汉",value:[114.31,30.52,199]}]
                    // 散点模式value代表的含义[经度，纬度，人数]
                    // itemStyle: {
                    //     emphasis: {
                    //         areaColor: '#DC143C'
                    //     }
                    // },
                    label: {
                        normal: {
                            show: false
                            // formatter: '{b}',
                            // textStyle: {
                            //     color: '#000'
                            // },
                            // show: true
                        },
                        emphasis: {
                            show: false
                        }
                    }
                }, {
                    name: '前5',
                    type: 'effectScatter',
                    mapType: 'china',
                    coordinateSystem: 'geo',
                    data: [],
                    symbolSize: 14,
                    showEffectOn: 'render',
                    rippleEffect: {
                        brushType: 'stroke'
                    },
                    hoverAnimation: true,
                    label: {
                        normal: {
                            show: false
                        },
                        emphasis: {
                            show: false
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: '#f4e925',
                            shadowBlur: 10,
                            shadowColor: '#333'
                        }
                    },
                    zlevel: 1
                }]
            }
        }
    },
    mounted() {
        this.initChart();
        this.requestData();
    },
    beforeDestroy() {
        if (!this.chart) {
            return
        }
        this.chart.dispose();
        this.chart = null;
    },
    methods: {
        requestData() {
            const params = {
                searchWords: this.searchWords,
            }
            this.$http.get(
                'http://lance.natapp1.cc/cityInfo',
                {params}
                ).then(res => {
                this.maxNums = 0
                console.log("requestData请求到的数据：", res.body)
                if (res.body.status === 200) {
                    // this.all = res.body.datas
                    this.options.series[0].data = res.body.datas
                    this.options.series[1].data = res.body.datas.sort(function (a, b) {
                        return b.value[2] - a.value[2];
                    }).slice(0, 5)
                    for (const item of res.body.datas) {
                        if (item.value[2] > this.maxNums) {
                            this.maxNums = item.value[2]
                        }
                    }
                    this.options.visualMap.min = this.minNums
                    this.options.visualMap.max = this.maxNums
                    // this.options.series[0].data = [{name:"厦门",value:[118.1,24.46,183]},{name:"武汉",value:[114.502869,30.556489,199]}]
                    this.chart.setOption(this.options)
                }
            }, err => {
                console.log(err)
            })
        },
        initChart() {
            this.chart = echarts.init(document.getElementById(this.id));
            // 把配置和数据放这里
            this.chart.setOption(this.options)
            // 自适应屏幕
            window.addEventListener("resize", () => { this.chart.resize()}, false);
        },
        randomValue() {
            return Math.round(Math.random()*1000);
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
            default: "数据分析师"
        }
    },
}
</script>