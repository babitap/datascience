<template>
  <div class="flex container">
    <div class="inputSection">
        <label class="flex xs12 form-label">Entity Name</label>
        <p v-if="readOnly" class="readonly-input">{{entity_name}}</p>
        <input v-if="!readOnly" class="flex xs12 form-input" v-bind:class="{ hasError: entityNameError !== '' }" v-model="entity_name" placeholder="Enter entity name here">
        <label v-if="entityNameError !== ''" class="error-label">{{entityNameError}}</label>
    </div>
    <div class="inputSection">
        <label class="flex xs12 form-label">Entity Type</label>
        <p v-if="readOnly" class="readonly-input">{{industry_name}}</p>
        <input v-if="!readOnly" class="flex xs12 form-input" v-bind:class="{ hasError: industryNameError !== '' }" v-model="industry_name" placeholder="Enter entity type here">
        <label v-if="industryNameError !== ''" class="error-label">{{industryNameError}}</label>
    </div>
      <div class="button-container">
        <va-button v-if="!readOnly" class="btn alignleft" @click="cancel">CANCEL</va-button>
        <va-button v-if="!readOnly" class="btn alignright" @click="update">UPDATE ENTITY</va-button>
        <va-button v-if="readOnly" class="btn alignright" @click="edit">EDIT ENTITY</va-button>
      </div>
      <div v-if="apiError !== ''" class="flex xs12 form-container error-container">
          <label class="error-label">{{apiError}}</label>
      </div>
      <div v-if="apiSuccess !== ''" class="flex xs12 form-container error-container">
          <label class="success-label">{{apiSuccess}}</label>
      </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
export default {
  name: "entity-management",
  components:{
  },
  props: {
    
  },
  data() {
    return {
      entity_id:0,
      entity_name:'',
      industry_name:'',
      entityNameError: '',
      industryNameError: '',
      apiError:'',
      apiSuccess:'',
      readOnly: true
    };
  },
  computed: {
    ...mapState({
      selectedEntity: state => state.user.selectedEntity
    })
  },
  mounted(){
    if(this.selectedEntity){
      this.entity_name = this.selectedEntity.entity_name
      this.industry_name = this.selectedEntity.industry_name
      this.entity_id = this.selectedEntity.id
    }
  },
  watch:{
    selectedEntity(newValue){
      if(newValue){
        this.entity_name = this.selectedEntity.entity_name
        this.industry_name = this.selectedEntity.industry_name
        this.entity_id = this.selectedEntity.id
      }
    }
  },
  methods:{
    ...mapActions({
      updateEntity: "user/updateEntity"
    }),
    update() {
        if(this.validateInput()){
            var param = {
                entityName: this.entity_name,
                industryName: this.industry_name,
                entityId: this.entity_id
            };

            this.updateEntity(param)
            .then(res => {
                if(res.success == false){
                    this.apiError = res.errorMessage;
                }
                else{
                  this.readOnly = true;
                }
            })
            .catch(err => {
                this.apiError = "Error update entity";
            })
            .finally(()=>{
            });
        }
    },
    edit(){
      this.readOnly = false
    },
    cancel(){
      this.readOnly = true
    },
    validateInput(){
        let isValid = true;
        var regex = new RegExp("^[a-zA-Z ]+$");

        if(this.entity_name === ''){
            this.entityNameError = 'Required';
            isValid = false;
        }
        else if( ! regex.test(this.entity_name) ){
            this.entityNameError = 'Only allow alphabet and space';
            isValid = false;            
        }
        else{
            this.entityNameError = '';
        }
        
        if(this.industry_name === ''){
            this.industryNameError = 'Required';
            isValid = false;
        }
        else if( ! regex.test(this.industry_name) ){
            this.industryNameError = 'Only allow alphabet and space';
            isValid = false;            
        }        
        else{
            this.industryNameError = '';
        }

        return isValid;
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  border: none;
  border-radius: 0.375rem;
  background: white;
  display: flex;
  flex-direction: column;
  min-width: 593px;
  max-width: 50%;
  padding-top: 3rem;

  & .inputSection {
    display: contents;

    & .readonly-input {
      padding-left: 0.75rem;
    }

    & .form-label {
      font-weight: 600;
    }

    & .form-input {
      border: 1px solid rgba(60, 60, 60, 0.26);
      border-radius: 4px;
      max-height: 2rem;
      color: #333333;

      &.hasError {
        border-color: #d43d27;
      }
    }
  }
}

.error-label {
  font-size: 0.75rem;
  color: #d43d27;
  font-weight: bold;
  margin-left: 0.25rem;
}

.success-label {
  font-size: 0.75rem;
  color: #089000;
  font-weight: bold;
  margin-left: 0.25rem;
}

.alignright {
  float: right;
}

.alignleft {
  float: left;
}

.form-label {
  font-size: 1rem;
  color: #34495e;
  display: block;
}

.button-container {
  margin-top: 0.75rem;
}
</style>