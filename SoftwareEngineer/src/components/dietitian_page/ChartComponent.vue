<template>
  <div ref="chart" style="width: 100%; height: 100%;"></div>
</template>

<script>
import * as echarts from "echarts";

export default {
  props: ["type"],  // 接受一个名为 "type" 的属性来决定图表类型
  mounted() {
    this.initChart();  // 组件挂载时初始化图表
  },
  watch: {
    type() {
      this.initChart();  // 监听 "type" 属性变化，更新图表
    },
  },
  methods: {
    initChart() {
      const chart = echarts.init(this.$refs.chart);  // 使用ECharts初始化图表
      const option = this.type === "pie" ? this.getPieOption() : this.getLineOption();  // 根据传入的类型选择图表配置
      chart.setOption(option);  // 设置图表配置
    },
    getPieOption() {
      return {
        title: { text: "营养分布", left: "center" },
        tooltip: { trigger: "item" },
        legend: { bottom: "0%", left: "center" },
        series: [
          {
            name: "食物成分",
            type: "pie",
            radius: "50%",
            data: [
              { value: 335, name: "蛋白质" },
              { value: 310, name: "脂肪" },
              { value: 234, name: "碳水化合物" },
              { value: 135, name: "纤维" },
              { value: 1548, name: "其他" },
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };
    },
    getLineOption() {
      return {
        title: { text: "每日热量消耗", left: "center" },
        tooltip: { trigger: "axis" },
        xAxis: {
          type: "category",
          data: ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
        },
        yAxis: { type: "value" },
        series: [
          {
            data: [820, 932, 901, 934, 1290, 1330, 1320],
            type: "line",
            smooth: true,
          },
        ],
      };
    },
  },
};
</script>

<style scoped>
/* 图表组件的样式，确保图表充满父容器 */
</style>