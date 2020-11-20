<template>
  <div class="benchmark">
    <div class="row row-equal">
      <!-- filter box -->
      <div class="flex xs12">
        <SchoolSelectionReport :filter_options="benchmarkSchoolFilterOptionsData"
                               :filtered_values="filtered_values"
                               @update_filter_value="get_new_filter_value"
                               @refresh_benchmark_data="refresh_benchmark_data"></SchoolSelectionReport>

      </div>
    </div>

    <div class="row row-equal">
      <!-- benchmark tabs -->
      <div class="flex xs12">
        <va-card style="overflow-x: auto;">
          <div class="row">
            <div class="flex xs12">
              <va-tabs grow v-model="selectedDataSetIndex" style="width: 100%;">
                <va-tab :key="0">
                  Enrolment Analysis
                </va-tab>
                <va-tab :key="1">
                  Staff Analysis
                </va-tab>
                <va-tab :key="2">
                  Financial Analysis
                </va-tab>
                <va-tab :key="3">
                  Academic Performance Analysis
                </va-tab>
                <va-tab :key="4">
                  Pricing Analysis
                </va-tab>
                <va-tab :key="5">
                  Benchmark Summary
                </va-tab>

              </va-tabs>
            </div>
          </div>

          <div class="row">
            <div class="flex xs12">
              <div v-if="benchmarkChartsData" class="customdivCharts">

                <div class="row row-equal">
                  <div v-if="selectedDataSetIndex === 0">
                    <BenchmarkReportMetric :benchmarkChartsData="benchmarkChartsData.student_enrol_analysis" :selectedTabIndex="selectedDataSetIndex" :key="selectedDataSetIndex">
                    </BenchmarkReportMetric>
                  </div>
                  <div v-else-if="selectedDataSetIndex === 1">
                    <BenchmarkReportMetric :benchmarkChartsData="benchmarkChartsData.staffing_analysis" :selectedTabIndex="selectedDataSetIndex" :key="selectedDataSetIndex">
                    </BenchmarkReportMetric>
                  </div>
                  <div v-else-if="selectedDataSetIndex === 2">
                    <BenchmarkReportMetric :benchmarkChartsData="benchmarkChartsData.financial_analysis" :selectedTabIndex="selectedDataSetIndex" :key="selectedDataSetIndex">
                    </BenchmarkReportMetric>
                  </div>
                  <div v-else-if="selectedDataSetIndex === 3">
                    <BenchmarkReportMetric :benchmarkChartsData="benchmarkChartsData.academicPerformance" :selectedTabIndex="selectedDataSetIndex" :key="selectedDataSetIndex">
                    </BenchmarkReportMetric>
                  </div>
                  <div v-else-if="selectedDataSetIndex === 4">
                    <BenchmarkReportMetric :benchmarkChartsData="benchmarkChartsData.pricing_analysis" :selectedTabIndex="selectedDataSetIndex" :key="selectedDataSetIndex">
                    </BenchmarkReportMetric>
                  </div>
                  <div v-else-if="selectedDataSetIndex === 5" class="flex xs12">
                    <BenchmarkSummary :summary_table="benchmarkChartsData.summary_table">
                    </BenchmarkSummary>
                  </div>
                  <div v-else>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </va-card>

      </div>
    </div>
  </div>    
</template>

<script>



import BenchmarkReportMetric from '../components/report-benchmark-metric' 
import BenchmarkSummary from '../components/summary-benchmark'
import SchoolSelectionReport from '../components/school-selection-report'
import { mapState, mapActions } from "vuex";
import { loadingService } from '@/app/shared/services/loading-service'

export default {
    name: "benchmark",
    components: {
        BenchmarkReportMetric,        
        BenchmarkSummary,
        SchoolSelectionReport,
    },
    data () {
        return {
          config: { value_field: 'value', label_field: 'label' },
          filtered_values: null,
          selectedDataSetIndex: 0,            
        }
    },
    // computed is a property, will always recaculated when its related (dependencies) variable changed, computed never have argument since its just a properties
    // triggered by another variable
    computed:{
        ...mapState({
            selectedEntity: state => state.user.selectedEntity,
            benchmarkSchoolFilterOptionsData: state=>state.benchmarkReport.benchmarkSchoolFilterOptionsData, 
            benchmarkSchoolFilterValuesData: state=>state.benchmarkReport.benchmarkSchoolFilterValuesData,
            benchmarkChartsData: state=>state.benchmarkReport.benchmarkChartsData,
        }), 
        focused_school_id: function(){
            if(this.selectedEntity !== null){
                return this.selectedEntity.industry_id
            }
            else{
                return null
            }            
      },

    },

    async created(){
      // load the benchmark fields structure !!      
      const promises = [
        this.load_benchmark_filters_data()  ,
        
      ];
      loadingService.showLoading(true)
      Promise.all(promises)
       .catch(err => {       
              console.log(err);    
              throw err; 
          })
        .finally(() => { loadingService.showLoading(false) })

      this.load_benchmark_report_charts_data()
    },
    watch: {
      // whenever benchmarkSchoolFilterValuesData changes, this function will run
        benchmarkSchoolFilterValuesData:function(){
          if (this.benchmarkSchoolFilterValuesData) {
                
                this.filtered_values = this.benchmarkSchoolFilterValuesData,
                this.load_benchmark_report_charts_data()
              }
        },
        focused_school_id: function(){
          if (this.focused_school_id) {

                
                const promises = [
                
                  this.load_benchmark_filters_data()             

                ];
                loadingService.showLoading(true)
                Promise.all(promises)
                .catch(err => {       
                console.log(err);    
                throw err; 
                })
                .finally(()=>{loadingService.showLoading(false)})
          
          }

          },


    },
    //method always run whenever having any events within the component
    methods: {
      ...mapActions(
            {
            loadBenchmarkSchoolFilterData: "benchmarkReport/getBenchmarkSchoolFilterData",
            loadBenchmarkReportChartsData: "benchmarkReport/getBenchmarkReportChartsData",

            }
      ),

      async load_benchmark_filters_data() {
        if (this.focused_school_id) {
              var param = {
                  "school_id": this.focused_school_id, 
              }
              await this.loadBenchmarkSchoolFilterData( param )
          }

        
      },

      get_value_out_of_list(list_of_dict, value_field){
            var tmp = []
            for(var i=0; i<list_of_dict.length; i++){
                tmp.push(list_of_dict[i][value_field])
            }
            return tmp
        },

      async load_benchmark_report_charts_data(){
        if( this.focused_school_id ){
          if (this.filtered_values) {
            
            var school_sector = this.get_value_out_of_list( this.filtered_values.schoolSectorDefaultOption, 'value' )
            var school_type = this.get_value_out_of_list( this.filtered_values.schoolTypeDefaultOption, 'value' )
            var school_state = this.get_value_out_of_list( this.filtered_values.stateDefaultOption, 'value' )
            var school_gender = this.filtered_values.schoolGenderDefaultOption['value']
            var selected_year = this.filtered_values.YearValue['value']
            var school_geolocation = this.get_value_out_of_list( this.filtered_values.geolocationDefaultOption, 'value' )
            var school_state = this.get_value_out_of_list( this.filtered_values.stateDefaultOption, 'value' )
            var enrolment_start_value = parseFloat(this.filtered_values.enrolmentRangeStartValue)
            var enrolment_end_value   = parseFloat(this.filtered_values.enrolmentRangeEndValue)           
            var distance_km = parseFloat(this.filtered_values.distanceKmValue)
            
            var param = {
              "school_id": this.focused_school_id, 
              "school_sector": school_sector,
              "school_type"  : school_type, 
              "school_state" : school_state, 
              "school_gender": school_gender, 
              "school_geolocation": school_geolocation,
              "enrolment_start_value" : enrolment_start_value, 
              "enrolment_end_value"   : enrolment_end_value,
              "distance_km": distance_km,
              "selected_year": selected_year,
            }
            await this.loadBenchmarkReportChartsData( param )
            }

        }

        },

      get_new_filter_value(new_filter_value){
              this.filtered_values = new_filter_value
          },

      refresh_benchmark_data(){
          loadingService.showLoading(true)
          this.load_benchmark_report_charts_data()
          .finally(()=>{loadingService.showLoading(false)})
        },

    }
}
</script>

<style lang="scss" scoped>
.customdivCharts {
  align-content: center;
  margin-left: 50px;
}
</style>
