
<template>
  <div class="row row-equal benchmarChats">
    <div class="flex xs12 md6 xl4 customCharts">
      <va-card class="chart">
        <plotly :data="position_chart_data.chart.chart_data" :layout="position_chart_data.chart.layout" />
      </va-card>
    </div>

    <div class="flex xs12 md6 xl4 customSummary">
     

      <va-card v-if="position_chart_data.infor" class="sumarycard">
        <h3>Metric Summary</h3> 
        
        <p>
          <b>Rating:</b>
          <span v-if="position_chart_data.infor.rating == 'unknown'" style="color: rgb(50, 100, 168); font-size: 40px;">&#63;</span>
          <span v-if="position_chart_data.infor.rating == 'bad'" style="color: rgb(237, 19, 19); font-size: 40px;">&#9746;</span>
          <span v-if="position_chart_data.infor.rating == 'good'" style="color: rgb(38, 237, 19); font-size: 40px;">&#10003;</span>
        </p>
            
        <p>


        </p>
        <p><b>Formula:</b> {{position_chart_data.infor.formular}}</p>
        <p><b>Position:</b> Your position is {{position_chart_data.infor.position}} out of {{position_chart_data.infor.total_samples}} samples.</p>
        <p>
          {{position_chart_data.infor.left_side_schools}}% of schools are above your school.
          {{position_chart_data.infor.right_side_schools}}% of schools are behind your school.
        </p>
      </va-card>
    </div>

  </div>
</template>



<script>
import {getFindexColors, getBinaryColors} from '../../../color_helper'

export default {
    props: {
    position_chart_data: Object,
  },
  data() {
    return {


    };
  },

  watch: {

    
  }, 
  methods:{

  },
};
</script>


<style lang="scss" scoped>
  .benchmarChats {
    margin: 0 !important;
  }

  .customCharts {
    align-content: center;
    margin-left: 20px;
    min-width: 900px;
  }

  .customSummary {
    align-content: center;
    margin-left: 20px;
    min-width: 200px;
  }

</style>

<style>

.card {
  border-radius: 3px;
  background-clip: border-box;
  border: 1px solid rgba(0, 0, 0, 0.125);
  box-shadow: 1px 1px 1px 1px rgba(0, 0, 0, 0.21);
  background-color: transparent;
}

</style>
