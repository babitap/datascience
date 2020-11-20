<template>
<div class="education-dashboard"> 
  <div class="row row-equal">
    <div class="flex xl6 xs30">
      <div class="row">
        <div
          class="flex sm6" 
          v-for="(info, idx) in infoTiles"
          :key="idx" >
          <va-card class="mb-4" :color="info.color">
            <p class="display-7"      style="color: #5f6e78;">{{ info.description }}</p>
            <p class="display-2 mb-0" style="color: #ee4823;">{{ info.value }}</p>          
            <p class="display-9"      style="color: #bac3c7;">{{ info.text }}</p>
          </va-card>
        </div>
      </div>
    </div>
  </div>

  <div class="row row-equal">
    <div class="flex xs12 md6 xl4" >
  
        <bar-chart-simple
        :cardTitle="this.enrolmentChart.card_title"
        :rawData="this.enrolmentChart.rawData" 
        :xColumn="this.enrolmentChart.xcolumn"
        :yColumns="this.enrolmentChart.ycolumns"
        :xAxisTitle="this.enrolmentChart.xaxis_title"
        :yAxisTitle="this.enrolmentChart.yaxis_title"  
      >
      </bar-chart-simple>
  
    </div>
    <div class="flex xs12 md6 xl4">
      <bar-chart-simple
        :cardTitle="this.staffChart.card_title"
        :rawData="this.staffChart.rawData" 
        :xColumn="this.staffChart.xcolumn"
        :yColumns="this.staffChart.ycolumns"
        :xAxisTitle="this.staffChart.xaxis_title"
        :yAxisTitle="this.staffChart.yaxis_title"  
      >
      </bar-chart-simple>
    </div>
   
    <div class="flex xs12 md6 xl4">
      <bar-chart-simple
        :cardTitle="this.incomeChart.card_title"
        :rawData="this.incomeChart.rawData" 
        :xColumn="this.incomeChart.xcolumn"
        :yColumns="this.incomeChart.ycolumns"
        :xAxisTitle="this.incomeChart.xaxis_title"
        :yAxisTitle="this.incomeChart.yaxis_title"  
      >
      </bar-chart-simple>
    </div>
  </div>
</div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import { loadingService } from '@/app/shared/services/loading-service'

export default {
  name: "education-dashboard",

  async created() {
    if (this.selectedEntity.industry_id && this.selectedEntity.industry_name === 'Education') {
      await this.loadDashboardJson(this.selectedEntity.industry_id);
    }
  },
  data() {
    return { 
      infoTiles: [{
        color: 'white',
        description: 'Teacher Efficiency Indicator',
        value: '-',
        text: 'Student / teacher ratio',
        icon: '',
      }, {
        color: 'white',
        description: 'Profitabity Indicator',
        value: '-',
        text: 'Recurrent income per student',
        icon: '',
      }],

      'enrolmentChart': {
            rawData: null, 
            xcolumn: 'calendarYear',
            //ycolumn: 'fullTimeEquivalentEnrolments',
            ycolumns: ['fullTimeEquivalentEnrolments'],
            card_title: 'Total Enrolment Number (FTE)',
            xaxis_title: '',
            yaxis_title: '',
          },
      'staffChart': {
            rawData: null, 
            xcolumn: 'calendarYear',
            //ycolumn: 'fullTimeEquivalentTeachingStaff',
            ycolumns: ['fullTimeEquivalentTeachingStaff','fullTimeEquivalentNonTeachingStaff'],
            card_title: 'Total Staff Number (FTE)',
            xaxis_title: '',
            yaxis_title: '',
          },
      'incomeChart': {
            rawData: null, 
            xcolumn: 'calendarYear',
            //ycolumn: 'fullTimeEquivalentTeachingStaff',
            ycolumns: [ 'incomeFeesChargesParent','incomeAusRecurrent','incomeStateRecurrent', 'incomeOtherPrivate'],
            card_title: 'Total Income',
            xaxis_title: '',
            yaxis_title: '',
          },
    };
  },

  computed: {
    ...mapState({
      selectedEntity: state => state.user.selectedEntity,
      dashboardJsonData: state => state.dashboard.dashboardJsonData
    })
  },
  methods: {
    ...mapActions({
      loadDashboardJson: "dashboard/getDashboardJsonData"
    }), 
    enable_info_blocks( ){
      const basicMetrics = this.dashboardJsonData.acaraDashboardQuery["basicMetrics"]

      this.infoTiles[0]['value'] = basicMetrics['studentTeacherRatio'].toFixed(2)
      this.infoTiles[1]['value'] = basicMetrics['recurrentIncomePerStudent'].toFixed(0)
    },
    enable_enrolment_chart(  ){
      if (this.dashboardJsonData.acaraDashboardQuery["basicYearlyInfo"]) {
        this.enrolmentChart.rawData = this.dashboardJsonData.acaraDashboardQuery["basicYearlyInfo"]
      }
    },
    enable_staff_chart(){
      if (this.dashboardJsonData.acaraDashboardQuery["basicYearlyInfo"]) {
        this.staffChart.rawData = this.dashboardJsonData.acaraDashboardQuery["basicYearlyInfo"]
      }
    },
    enable_income_chart(){
      if (this.dashboardJsonData.acaraDashboardQuery["finance"]) {
        this.incomeChart.rawData = this.dashboardJsonData.acaraDashboardQuery["finance"]
      }
    },
  },
  watch: {
    async selectedEntity( new_val) {
      if (this.selectedEntity.industry_id && this.selectedEntity.industry_name === 'Education') {
        //console.log(" in watch selectedSchool(), "+this.selectedSchool.acaraId)
        await this.loadDashboardJson(this.selectedEntity.industry_id)
      }
    },

    dashboardJsonData() {
      if (this.dashboardJsonData["acaraDashboardQuery"]) {        
        this.enable_info_blocks()
        this.enable_enrolment_chart()
        this.enable_staff_chart()
        this.enable_income_chart()
      }      
    }
  }
};
</script>

<style lang="scss">
  .row-separated {
    .flex + .flex {
      border-left: 1px solid #e3eaeb;
    }

    @include media-breakpoint-down(xs) {
      p:not(.display-2) {
        font-size: 0.875rem;
      }
    }
  }

  .education-dashboard {
    .va-card__header--over {
      @include media-breakpoint-up(md) {
        padding-top: 0 !important;
      }
    }

    .va-card__image {
      @include media-breakpoint-up(md) {
        padding-bottom: 0 !important;
      }
    }

    .va-card__body {
      @include media-breakpoint-up(md) {
        min-height: 150px;
      }
    }

    .svg-container {
      @include media-breakpoint-up(xs) {
        max-height: 550px;
        max-width: 350px;
      }
    }
  }
</style>
