<template>
<div class="benchmark">
    <div class="row row-equal">
    <!-- filter box -->
      <div class="flex xs12">
            <school-selection 
                :filter_options="benchmarkSchoolFilterOptionsData"
                :filtered_values="filtered_values"
                @update_filter_value="get_new_filter_value"
                @refresh_comparable_schools_data="refresh_comparable_schools_data"
                ></school-selection>

      </div>
    </div>
    <div class="row row-equal">
        <!-- benchmark tabs -->
        <div class="flex xs12">
            <va-card style="overflow-x: auto;">
                <div class="row">
                    <div class="flex xs12">
                        <va-tabs grow v-model="selectedDataSetIndex" style="width: 100%;">
                            <va-tab
                            v-for="dataset in benchmarkStructureData"
                            :key="dataset.value"
                            >
                            {{dataset.label}}
                            </va-tab>
                        </va-tabs>
                    </div>
                </div>
    
                <div class="row">
                    <div class="flex xs12">
                        <va-button-toggle
                            outline
                            :options="available_metrics"
                            v-model="selectedMetricValue"
                            color="primary"
                        />
                        <button-group :input_items="available_submetrics" 
                                        :value_field="config.value_field"
                                        :label_field="config.label_field"
                                        :deselected_values="deselectedSubMetricValues"
                                        @toggle_submetric_value="toggle_submetric_value"
                        >
                        </button-group>
                        <div class="customdivCharts" >
                        <benchmark-charts 
                            :benchmarkChartsData="benchmarkChartsData">
                        </benchmark-charts>
                        </div>
                    </div>
                </div>
            </va-card>

        </div>
    </div>
</div>    
</template>

<script>

import ButtonGroup from '../components/button-group'
import BenchmarkCharts from './benchmark-charts'
import SchoolSelection from '../components/school-selection'
import { mapState, mapActions } from "vuex";
import { loadingService } from '@/app/shared/services/loading-service'

export default {
    name: "benchmark",
    components:{
        ButtonGroup,
        BenchmarkCharts,
        SchoolSelection,
    },
    data () {
        return {
            config:{ value_field:'value' , label_field:'label' },

            selectedDataSetIndex : null, 
            selectedMetricValue: null,
            deselectedSubMetricValues: [],

            filtered_values: null, 
        }
    },
    computed:{
        ...mapState({
            selectedEntity: state => state.user.selectedEntity,
            benchmarkStructureData: state => state.benchmark.benchmarkStructureData,
            benchmarkChartsData: state=>state.benchmark.benchmarkChartsData,
            benchmarkSchoolFilterOptionsData: state=>state.benchmark.benchmarkSchoolFilterOptionsData, 
            benchmarkSchoolFilterValuesData: state=>state.benchmark.benchmarkSchoolFilterValuesData, 
            benchmarkComparableSchools: state=>state.benchmark.benchmarkComparableSchools,
        }), 
        focused_school_id: function(){
            if(this.selectedEntity !== null){
                return this.selectedEntity.industry_id
            }
            else{
                return null
            }
            
        },
        comparable_school_ids:function(){
            if( this.benchmarkComparableSchools  ){
                return this.get_value_out_of_list( this.benchmarkComparableSchools, 'id' )
            }
            else{
                return []
            }
            //return [46483,46621,46746,47485,47577,47913]
        },
        focused_dataset:function(){
            if( this.benchmarkStructureData !== null ){
                return this.benchmarkStructureData[this.selectedDataSetIndex]
            }
            else{
                return null 
            }
        }, 
        available_metrics: function(){
          if (this.focused_dataset) {
            console.log("available_metrics")
            console.log(this.focused_dataset.metrics)
                return this.focused_dataset.metrics
            }
            else{
                return null 
            }
        }, 
        focused_metric: function(){
            if( this.available_metrics!== null){
                for(var i=0; i<this.available_metrics.length; i++){
                    if( this.available_metrics[i].value == this.selectedMetricValue){
                        return this.available_metrics[i]
                    }
                }
                return null 
            }
            else{
                return null 
            }
        },
        selected_metric_model: function(){
            if(this.focused_metric!== null){
                return this.focused_metric.model
            }
            else{
                return null 
            }
        },
        selected_metric_field: function(){
            if(this.focused_metric!== null){
                return this.focused_metric.field
            }
            else{
                return null
            }
        },
        available_submetrics: function(){
            if(this.focused_metric!== null){
                return this.focused_metric.subMetrics
            }
            else{
                return null 
            }
        },
        selected_submetrics_fields: function(){
            if( this.available_submetrics !== null ){
                var temp = []
                for(var i=0; i<this.available_submetrics.length; i++){
                    if(this.deselectedSubMetricValues.includes( this.available_submetrics[i].value ) )
                    {

                    }
                    else{
                        temp.push( this.available_submetrics[i].field )
                    }
                }
                return temp
            }
            else{
                return null
            }
        },
    },

    async created(){
      // load the benchmark fields structure !! 
      const promises = [
        this.loadBenchmarkStructureData(),
        this.load_benchmark_filters_data(),
        this.load_comparable_schools_data(),
        this.load_benchmark_charts_data()
      ];
      loadingService.showLoading(true)
      Promise.all(promises)
       .catch(err => {       
              console.log(err);    
              throw err; 
          })
      .finally(()=>{loadingService.showLoading(false)})
    },
    watch: {
        benchmarkSchoolFilterValuesData:function(){
            if( this.benchmarkSchoolFilterValuesData ){
                this.filtered_values = this.benchmarkSchoolFilterValuesData
            }
        },
        comparable_school_ids:function(){
            if( this.comparable_school_ids ){
              loadingService.showLoading(true)
              this.load_benchmark_charts_data()
              .catch(err => {       
              console.log(err);    
              throw err; 
               })
              .finally(()=>{loadingService.showLoading(false)})
            }
        },
        benchmarkStructureData:function(){
            //console.log("watch benchmarkStructureData")
            if(this.benchmarkStructureData){
                this.selectedDataSetIndex = 0
            }
        },
        selectedDataSetIndex: function(){
          console.log("watch selectedMetricValue")
          console.log(this.benchmarkStructureData[this.selectedDataSetIndex].metrics[0].value)
            this.selectedMetricValue = this.benchmarkStructureData[this.selectedDataSetIndex].metrics[0].value

        }, 
        focused_school_id: function(){
            if( this.focused_school_id ){
              const promises = [
                this.load_benchmark_filters_data(),
                this.load_benchmark_charts_data()
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
        selectedMetricValue: function(){
            //console.log("watch selectedMetricValue")
            if( this.focused_school_id ){
              loadingService.showLoading(true)
              this.load_benchmark_charts_data()
              .catch(err => {       
              console.log(err);    
              throw err; 
              })
              .finally(()=>{loadingService.showLoading(false)})
            }
        },
        deselectedSubMetricValues:function(){
            //console.log("watch deselectedSubMetricValues")
            if( this.focused_school_id ){
              loadingService.showLoading(true)
              this.load_benchmark_charts_data()
              .catch(err => {       
              console.log(err);    
              throw err; 
              })
              .finally(()=>{loadingService.showLoading(false)})
            }
        },
    },
    methods: {
        ...mapActions(
            {
                loadBenchmarkStructureData: "benchmark/getBenchmarkStructureData", 
                loadBenchmarkChartsData  : "benchmark/getBenchmarkChartsData",
                loadBenchmarkSchoolFilterData: "benchmark/getBenchmarkSchoolFilterData",
                loadBenchmarkComparableSchoolsData:"benchmark/getBenchmarkComparableSchoolsData",
            }
        ),
        // function used to react to click event in button-group
        toggle_submetric_value( clicked_submetric_value ){
            if( this.deselectedSubMetricValues.includes(clicked_submetric_value) ){
                const index = this.deselectedSubMetricValues.indexOf(clicked_submetric_value)
                if (index > -1) {
                    this.deselectedSubMetricValues.splice(index, 1)
                }
            }
            else{
                this.deselectedSubMetricValues.push(clicked_submetric_value)
            }
        },
        get_new_filter_value(new_filter_value){
            this.filtered_values = new_filter_value
        },

        async load_benchmark_charts_data(){

            if( (this.focused_school_id !== null ) & (this.comparable_school_ids !== null)  & (this.selected_metric_model !== null) ){
                var param = {
                    "school_id": this.focused_school_id, 
                    "comparable_school_ids":this.comparable_school_ids, 
                    "model": this.selected_metric_model, 
                    "metric_field": this.selected_metric_field, 
                    "submetrics_fields": this.selected_submetrics_fields
                }
                console.log("send loadBenchmarkChartsData")
                console.log(param)
                await this.loadBenchmarkChartsData( param )
            }

        },
        get_value_out_of_list(list_of_dict, value_field){
            var tmp = []
            for(var i=0; i<list_of_dict.length; i++){
                tmp.push(list_of_dict[i][value_field])
            }
            return tmp
        },
        async load_comparable_schools_data(){
            console.log('focused_school_id:'+ this.focused_school_id)
            if( this.focused_school_id ){
                if( this.filtered_values ){
                    var school_sector = this.get_value_out_of_list( this.filtered_values.schoolSectorDefaultOption, 'value' )
                    var school_type = this.get_value_out_of_list( this.filtered_values.schoolTypeDefaultOption, 'value' )
                    var school_state = this.get_value_out_of_list( this.filtered_values.stateDefaultOption, 'value' )
                    var school_gender = this.get_value_out_of_list( this.filtered_values.schoolGenderDefaultOption, 'value' )
                    var school_geolocation = this.get_value_out_of_list( this.filtered_values.geolocationDefaultOption, 'value' )
                    var school_state = this.get_value_out_of_list( this.filtered_values.stateDefaultOption, 'value' )
                    var enrolment_start_value = this.filtered_values.enrolmentRangeStartValue
                    var enrolment_end_value   = this.filtered_values.enrolmentRangeEndValue
                    var distance_km = this.filtered_values.distanceKmValue
                    var param = {
                        "school_id": this.focused_school_id, 
                        "school_sector": school_sector,
                        "school_type"  : school_type, 
                        "school_state" : school_state, 
                        "school_gender": school_gender, 
                        "school_geolocation": school_geolocation,
                        "enrolment_start_value" : enrolment_start_value, 
                        "enrolment_end_value"   : enrolment_end_value,
                        "distance_km"  : distance_km,
                    }
                    await this.loadBenchmarkComparableSchoolsData( param )
                }

            }
        }, 
        async load_benchmark_filters_data(){
            if( this.focused_school_id ){
                var param = {
                    "school_id": this.focused_school_id, 
                }
                await this.loadBenchmarkSchoolFilterData( param )
            }
        },
        refresh_comparable_schools_data(){
          loadingService.showLoading(true)
          this.load_comparable_schools_data()
          .finally(()=>{loadingService.showLoading(false)})
        }
    }
}
</script>

<style lang="scss" scoped>
.customdivCharts {
  align-content: center;
  margin-left: 50px;
}
</style>
