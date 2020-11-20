<template>
  <div >
    <va-card class="chart" >
        <p class="display-7" style="color: #5f6e78;">{{ cardTitle }}</p>
        <plotly
            :data="plotlyData.data" :layout="plotlyData.layout" :options="plotlyData.options" :autoResize="plotlyData.autoResize" 
        />
    </va-card>
  </div>    
</template>

<script>
import {getFindexColors, getBinaryColors} from '../../../color_helper'

export default {
  props:{
    cardTitle: null, 
    rawData: null, 
    xColumn: null, 
    yColumns: null,
    focusedColumn: null, 
    xAxisTitle: null, 
    yAxisTitle: null, 
  },
  data() {
    return {

      plotlyData:{
        data:[],
        layout:{
          autosize : true, 
          //height: 330,
          //width : 470,
          plot_bgcolor:"#FFFFFF",
          //paper_bgcolor:"grey",
          //title: "My graph",
          margin : {'t': 40,'l':40, 'r':40, 'b':40}, 
          xaxis : { title: null , 
                    tickvals:[],
                    showgrid: true 
                    },
          yaxis : { title: null ,showgrid: true },
          barmode: 'stack',
          showlegend: false, 
          legend:{ orientation:  'h',
                   x: 0,
                   y: 1.1,
                   bgcolor : 'rgba(0,0,0,0)'
                   }
        }, 
        options: { displaylogo: false }, 
        autoResize : true, 
      } , 
      traceTemplate:{
        x: [], 
        y: [], 
        text:[], 
        textposition : 'auto',
        name: null,
        type:'bar',
      },
    };
  },

  watch: {

    rawData: function( new_value, old_value ){
      if(new_value){
        if(this.yColumns){
          var arrayLength = new_value.length
          var binary_colors = getBinaryColors()
          var focused_color = binary_colors['FOCUSED']
          var not_focused_color = binary_colors['NOT_FOCUSED']

          // stacked bar chart  
          var x_vals = []
          this.plotlyData.data = []
          for( var j = 0; j<this.yColumns.length; j++ )
          {
            var column_name = this.yColumns[j]


            for (var i = 0; i < arrayLength; i++)
            {
              // initialize the trace data
              var trace = JSON.parse(JSON.stringify(this.traceTemplate))

              var x_value = new_value[i][this.xColumn]
              var y_value = new_value[i][column_name]
              trace.x.push( x_value )
              x_vals.push(x_value)

              if(y_value){
                trace.y.push( y_value )
                trace.text.push(y_value.toString())
              }
              else{
                trace.y.push( null )
                trace.text.push(null)
              }
              
              //if(j==0){
              //  x_tickvals.push(x_value.toString())
              //}
              //trace.name = column_name
              if(new_value[i][this.focusedColumn]){
                trace.marker = { color:  focused_color  }
              }
              else{
                trace.marker = { color:  not_focused_color  }
              }

              this.plotlyData.data.push( trace )
            }

            

          }
          var sorted_x_values =x_vals.sort(function(a, b){return a - b})
          this.plotlyData.layout.xaxis.tickvals = sorted_x_values

        }
        else{

        }

          
        // some extra work: 
        this.plotlyData.layout.xaxis.title = this.xAxisTitle; 
        this.plotlyData.layout.yaxis.title = this.yAxisTitle; 
      }

    },
  }, 
  methods:{

  },
};
</script>

<style>
.card {
  border-radius: 3px;
  background-clip: border-box;
  border: 1px solid rgba(0, 0, 0, 0.125);
  box-shadow: 1px 1px 1px 1px rgba(0, 0, 0, 0.21);
  background-color: transparent;
}

</style>
