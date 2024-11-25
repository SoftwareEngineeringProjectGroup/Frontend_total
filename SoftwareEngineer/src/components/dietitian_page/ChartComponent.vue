<template>
  <div ref="chart" style="width: 100%; height: 100%;"></div>
</template>

<script>
import * as echarts from "echarts";

export default {
  props: ["type"], // Accepts a prop named "type" to determine the chart type
  mounted() {
    this.initChart(); // Initialize the chart when the component is mounted
  },
  watch: {
    type() {
      this.initChart(); // Watch for changes in the "type" prop and update the chart
    },
  },
  methods: {
    initChart() {
      const chart = echarts.init(this.$refs.chart); // Initialize the chart with ECharts
      const option = this.type === "pie" ? this.getPieOption() : this.getLineOption(); // Select the chart configuration based on the type
      chart.setOption(option); // Set the chart configuration
    },
    getPieOption() {
      return {
        title: { text: "Nutritional Distribution", left: "center" },
        tooltip: { trigger: "item" },
        legend: { bottom: "0%", left: "center" },
        series: [
          {
            name: "Food Components",
            type: "pie",
            radius: "50%",
            data: [
              {value: 335, name: "Protein"},
              {value: 310, name: "Fat"},
              {value: 234, name: "Carbohydrates"},
              {value: 135, name: "Fiber"},
              {value: 1548, name: "Others"},
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
        title: {text: "Daily Calorie Consumption", left: "center"},
        tooltip: {trigger: "axis"},
        xAxis: {
          type: "category",
          data: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        },
        yAxis: {type: "value"},
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
/* Styles for the chart component to ensure it fills the parent container */
</style>
