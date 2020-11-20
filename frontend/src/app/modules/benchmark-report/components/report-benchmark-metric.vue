<template>
  <div class="container filter">
    <div class="selectionContainer">
      <div v-if="benchmarkChartsData != []" class="flex xs12">
        <BarChartPosition v-for="metric in benchmarkChartsData" :position_chart_data="metric">
        </BarChartPosition>
      </div>
      <div v-if="benchmarkChartsData.length == 0" class="flex xs12">
        There is no data matched with above filters.
      </div>
    </div>
  </div>
</template>
<script>
import BarChartPosition from '../components/bar-chart-position-report.vue';
  export default {
    name: 'enrolmentBenchmark',
    components: {
      BarChartPosition,
    },
    // data get from parent
    props: {
      benchmarkChartsData: Array,
      selectedTabIndex: Number
    },
    // data by default (initial value) when loading the component
    data() {
      return {
      };
    },
    computed:{
    },
    created: function () {
      console.log('selectedTabIndex: ' + this.selectedTabIndex);
      console.log('benchmarkChartsData: ' + this.benchmarkChartsData);
    },
    watch: {
    },
    methods: {
    }
  };
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss" scoped>
  .selectionContainer {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    padding: 10px;
  }
</style>
