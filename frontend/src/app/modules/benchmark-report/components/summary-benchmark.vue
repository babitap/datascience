<template>
  <div class="container filter">
    <div class="selectionContainer">
      <div class="flex xs12">
        <va-data-table :fields="['Bechmark Type', 'Your Shool Value', 'Median value of Other Schools','Rating']"
                       :data="summary_table"
                       :per-page="10">
          <template slot="actions" slot-scope="props">
            <va-button small @click="">
              SELECT
            </va-button>
          </template>
        </va-data-table>
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
      summary_table: Array
      //filtered_values: Object
    },
    // data by default (initial value) when loading the component
    data() {
      return {
      };
    },
    computed:{
    },
    watch: {
    },
    methods: {
    }
  };
</script>
<style lang="scss" scoped>
  .selectionContainer {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    padding: 10px;
  }
</style>
