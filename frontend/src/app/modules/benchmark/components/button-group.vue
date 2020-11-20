<template>
<div class="row buttonGroup" v-if="input_items">
    <div v-for="item in items" :key="item.value">
        <va-button small icon="ion-md-checkmark ion" v-if="deselected_values.includes(item.value)"
                color="gray" v-on:click="click_button(item)"
        > {{ item.label }} </va-button>

        <va-button small icon="ion-md-close ion" v-else
                color="info" v-on:click="click_button(item)"
        > {{ item.label }} </va-button>
    </div>
</div>
</template>

<script>
export default {
    name: 'button-group',
    props:{
        input_items: Array, 
        value_field: String, 
        label_field: String,
        deselected_values : Array, 
    }, 
    computed:{
        items: function(){
            var temp = []
            for(var i=0; i<this.input_items.length; i++){
                temp.push( { value: this.input_items[i][this.value_field] , 
                             label: this.input_items[i][this.label_field] 
                            } )
            }
            return temp
        }
    },
    methods: {
        click_button( clicked_item ){
            this.$emit("toggle_submetric_value", clicked_item.value )
            /*
            var deselected_values_new = this.deselected_values

            if(deselected_values_new.includes(clicked_item.value)){
                var temp = []
                for(var i=0; i<deselected_values_new.length; i++){
                    if( deselected_values_new[i] == clicked_item.value )
                    {
                        
                    }else{
                        temp.push(deselected_values_new[i] )
                    }
                }
                deselected_values_new = temp
            }
            else{
                
                deselected_values_new.push(clicked_item.value)
            }
            this.$emit("change_deselected_values", deselected_values_new )
            */
        }, 
    }
}
</script>
<style lang="scss" scoped>
.buttonGroup {
  margin: 0 !important;
}
</style>