<template>
    <div class="row row-equal benchmarChats">
        <div class="flex xs12 md6 xl4 customCharts">        
            <bar-chart-position
                :cardTitle="this.positionChart.card_title"
                :rawData="this.positionChart.rawData" 
                :xColumn="this.positionChart.xcolumn"
                :yColumns="this.positionChart.ycolumns"
                :focusedColumn="this.positionChart.focusedColumn"
                :xAxisTitle="this.positionChart.xaxis_title"
                :yAxisTitle="this.positionChart.yaxis_title"  
            >
            </bar-chart-position>
        </div>
        <div class="flex xs12 md6 xl4 customCharts" >
            <line-chart-trend
                :cardTitle="this.trendChart.card_title"
                :rawData="this.trendChart.rawData" 
                :xColumn="this.trendChart.xcolumn"
                :yColumn="this.trendChart.ycolumn"
                :idColumn="this.trendChart.idColumn"
                :lineDataColumn="this.trendChart.lineDataColumn"
                :focusedColumn="this.trendChart.focusedColumn"
                :xAxisTitle="this.trendChart.xaxis_title"
                :yAxisTitle="this.trendChart.yaxis_title"  
            >
            </line-chart-trend>
        </div>

    </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

import BarChartPosition from '../components/bar-chart-position.vue';
import LineChartTrend from '../components/line-chart-trend.vue';

export default {
    name: 'benchmark-charts',
    components:{
        BarChartPosition,
        LineChartTrend,
    },
    data() {
        return {
            positionChart : {
                rawData: null, 
                xcolumn: 'id',
                //ycolumn: 'fullTimeEquivalentEnrolments',
                ycolumns: ['value'],
                focusedColumn: 'focused',
                card_title: 'Latest Position',
                xaxis_title: '',
                yaxis_title: '',                
            },
            trendChart : {
                rawData: null, 
                xcolumn: 'calendarYear',
                ycolumn: 'value',
                idColumn: 'id',
                focusedColumn: 'focused',
                lineDataColumn: 'lineData',
                card_title: 'Long-term Trend',
                xaxis_title: '',
                yaxis_title: '',
            },
        }
    },
    props: {
        benchmarkChartsData  : Object,
    },
    watch:{
        benchmarkChartsData:function(){
            if( this.benchmarkChartsData ){
                if( "position" in this.benchmarkChartsData ){
                    this.positionChart.rawData = this.benchmarkChartsData["position"]
                }
                else{
                    this.positionChart.rawData = null 
                }

                if( "trend" in this.benchmarkChartsData ){
                    this.trendChart.rawData = this.benchmarkChartsData["trend"]
                }
                else{
                    this.trendChart.rawData = null 
                }
            }
            else{
                this.positionChart.rawData = null 
                this.trendChart.rawData = null 
            }
        },
    },
    methods: {
    }
}
</script>

<style lang="scss" scoped>
.benchmarChats {
  margin: 0 !important;
}

.customCharts {
  align-content: center;
  margin-left: 20px;
  min-width: 400px;
}
</style>