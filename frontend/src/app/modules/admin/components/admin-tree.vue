<template>
<div class="flex xs12">

  <modals-container />
  
  <v-dialog
    @before-opened="dialogEvent('before-open')"
    @before-closed="dialogEvent('before-close')"
    @opened="dialogEvent('opened')"
    @closed="dialogEvent('closed')"
   
    />
    
        <div class="flex xs12">
            <va-card style="overflow-x: auto;">
                    <va-tree-root>
                        <va-tree-category isOpen v-for="industry in treeDataJson" :label="industry.label" :key="industry.value" icon="ion ion-md-school">
                        <va-tree-category isOpen  v-for="entity in industry.entities" :label="entity.label" :key="entity.value" icon="ion ion-md-business">  
                            <va-tree-node :highlighted="industry.value===selected.industry_value &&entity.value===selected.entity_value &&user_group.value===selected.user_group_value"
                             v-for="user_group in entity.user_groups" :label="user_group.label" :key="user_group.value" icon="ion ion-md-people" >            
                                <a @click="click_user_group(industry.value, entity.value ,user_group.value)" >{{ user_group.label }}</a>
                            </va-tree-node> 
                            <va-tree-node icon="ion ion-md-people">
                                <a @click="click_add_group( industry.value, industry.label,entity.value, entity.label )"                                  
                                > + Group</a>
                            </va-tree-node>    
                        </va-tree-category>
                        </va-tree-category>
                    </va-tree-root>
            </va-card>
        </div>
</div>
</template>

<script>
import AddGroupModal from './add-group-modal.vue'


export default {
    name: "admin-tree",
    components:{
        AddGroupModal,
    },
    props: {
        treeData: Array,
        selected: Object, 
    },
    data: function() {
        return {

            showAddUserGroupDialog: false, 

            treeDataJson:  [
                        {
                            value:'education' , 
                            label:'Education' ,
                            entities: []
                    }
                ],     
            
            };
    },
    created(){
        //this.treeDataJson = self.treeDataJsonTemplate
    },
    watch:{
        treeData(new_value){
            if(new_value!==null&&new_value!==undefined){
                this.treeDataJson = new_value
            }
            else{
                this.treeDataJson =  [
                                        {
                                                value:'education' , 
                                                label:'Education' ,
                                                entities: []
                                        }
                                    ]
            }
        },
    },
    methods: 
    {
        click_user_group:function( industry_value ,entity_value, user_group_value ){
            this.$emit( "change_user_group", { industry_value: industry_value, entity_value: entity_value, user_group_value:  user_group_value }  )
        },
        click_add_group: function( industry_value, industry_label, entity_value, entity_label ){
            // add a new user group, we need popup a dialog 
            console.log('click add-group button')
            this.$modal.show(AddGroupModal, 
                {
                    title: 'Add user group',
                    text: 'Create a new user group under \' '+ entity_label + ' \'',
                    
                    industry_id: industry_value,
                    entity_id: entity_value, 
                }, 
                {
                    isAutoHeight: true, 
                    resizable: true,
                    adaptive: true,
                    draggable: true,
                },
                     
            )
            //this.$emit( "add_user_group",  { industry_value: industry_value, entity_value: entity_value } )
        }, 

        dialogEvent (eventName) {
            console.log('Dialog event: ' + eventName)
        }
    }
}
</script>