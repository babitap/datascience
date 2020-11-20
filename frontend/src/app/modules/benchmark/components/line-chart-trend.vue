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
    idColumn: null, 
    focusedColumn: null, 
    lineDataColumn: null, 

    xColumn: null, 
    yColumn: null, 

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
          xaxis : { title: null ,tickvals:[],showgrid: true },
          yaxis : { title: null ,showgrid: true },
          //barmode: 'stack',
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
        type:'scatter',
        mode: 'lines+markers',
      },
    };
  },

  watch: {

    rawData: function( new_value, old_value ){
      if(new_value !== null ){
        // initialize everything 
        this.plotlyData.data = []

        var x_vals = []
        var binary_colors = getBinaryColors()
        var focused_color = binary_colors['FOCUSED']
        var not_focused_color = binary_colors['NOT_FOCUSED']

        var column_name = this.yColumn

        // loop through all IDs/lines
        for( var j=0; j<new_value.length; j++ )
        {
          var trace = JSON.parse(JSON.stringify(this.traceTemplate))

          var id = new_value[j][this.idColumn]
          var focused = new_value[j][this.focusedColumn]
          var chosed_color = not_focused_color
          if(focused){
            chosed_color = focused_color
          }
          var lineData = new_value[j][this.lineDataColumn]
          for( var i=0; i<lineData.length; i++ ){
            var x_value = lineData[i][this.xColumn]
            var y_value = lineData[i][this.yColumn]
            trace.x.push( x_value )
            x_vals.push(x_value)
            trace.y.push( y_value )
            trace.text.push(y_value.toString())
          }
          trace.name = id.toString()
          trace.marker = { color:  chosed_color  }
          this.plotlyData.data.push( trace )
        }

        x_vals = Array.from(new Set(x_vals))
        var sorted_x_values =x_vals.sort(function(a, b){return a - b})

        this.plotlyData.layout.xaxis.tickvals = sorted_x_values

          
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
