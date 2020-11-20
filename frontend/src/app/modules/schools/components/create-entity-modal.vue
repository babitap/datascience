<template>
  <va-card class="container" style="overflow-x: auto; overflow-y: visible;">
    <p class="display-5" style="color: #5f6e78;">{{title}}</p>

    <div class="body">
      <va-input
        v-model="entity_name"
        label="New Entity Name"
        placeholder="Enter entity name here"
        :error="!!entityNameError.length"
        :error-messages="entityNameError"
      />
      <va-input
        v-model="industry_name"
        label="New Entity Type"
        placeholder="Enter entity type here"
        :error="!!industryNameError.length"
        :error-messages="industryNameError"
      />
      <va-button class="btn alignleft" @click="cancel">CANCEL</va-button>
      <va-button
        class="btn alignright"
        @click="save"
      >SAVE</va-button>
    </div>
  </va-card>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "create-entity-modal",
  props: {
    title: String
  },
  data() {
    return {
      entity_name: "",
      industry_name: "",
      entityNameError: [],
      industryNameError: [],
      apiError:""
    };
  },
  computed: {
    ...mapState({
      adminTreeJsonData: state => state.admin.adminTreeJsonData
    }),
    empty_warning_label() {
      if (this.usergroup_name === "") {
        return true;
      } else {
        return false;
      }
    }
  },

  methods: {
    ...mapActions({
      createEntity: "user/createEntity"
    }),

    cancel() {
      this.$emit("close");
    },
    save() {
        if(this.validateInput()){
            var param = {
                entityName: this.entity_name,
                industryName: this.industry_name
            };

            this.createEntity(param)
            .then(res => {
                if(res.success == true){
                    this.$emit("close");
                }
                else{
                    this.apiError = res.errorMessage;
                }
            })
            .catch(err => {
                this.apiError = "Error create entity";
            })
            .finally(()=>{
            });
        }
    },
    validateInput(){
        let isValid = true;
        var regex = new RegExp("^[a-zA-Z ]+$");

        if(this.entity_name === ''){
            this.entityNameError.push('Required');
            isValid = false;
        }
        else if( ! regex.test(this.entity_name) ){
            this.entityNameError.push('Only allow alphabet and space');
            isValid = false;            
        }
        else{
            this.entityNameError = [];
        }
        
        if(this.industry_name === ''){
            this.industryNameError.push('Required');
            isValid = false;
        }
        else if( ! regex.test(this.industry_name) ){
            this.industryNameError.push('Only allow alphabet and space');
            isValid = false;            
        }              
        else{
            this.industryNameError = [];
        }

        return isValid;
    }
  }
};
</script>

<style scoped>
.container {
  box-shadow: none !important;
}

.body {
  margin-top: 1rem;
}

.alignright {
  float: right;
}

.alignleft {
  float: left;
}
</style>