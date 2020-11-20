<template>
  <va-card class="container" style="overflow-x: auto; overflow-y: visible;">
    <p class="display-5" style="color: #5f6e78;">{{title}}</p>

    <div class="body">
      <div class="inputSection">
        <label class="flex xs12 form-label">Name</label>
        <input class="flex xs12 form-input" v-bind:class="{ hasError: nameError !== '' }" v-model="name" placeholder="Enter report name here">
        <label v-if="nameError !== ''" class="error-label">{{nameError}}</label>
      </div>
      <div class="inputSection">
        <label class="flex xs12 form-label">Workspace Id</label>
        <input class="flex xs12 form-input" v-bind:class="{ hasError: workspaceIdError !== '' }" v-model="workspaceId" placeholder="Enter workspace id here">
        <label v-if="workspaceIdError !== ''" class="error-label">{{workspaceIdError}}</label>
      </div>
      <div class="inputSection">
        <label class="flex xs12 form-label">Report Id</label>
        <input class="flex xs12 form-input" v-bind:class="{ hasError: reportIdError !== '' }" v-model="reportId" placeholder="Enter report id here">
        <label v-if="reportIdError !== ''" class="error-label">{{reportIdError}}</label>
      </div>
      <div class="inputSection">
        <label class="flex xs12 form-label">Permission</label>
        <v-select v-bind:class="{ hasError: permissionError !== '' }" label="name" v-model="permission" :options="permissionOptions"></v-select>
        <label v-if="permissionError !== ''" class="error-label">{{permissionError}}</label>
      </div>
      <div class="inputSection">
        <label class="flex xs12 form-label">Category</label>
        <v-select v-bind:class="{ hasError: categoryError !== '' }" label="name" v-model="category" :options="categoryOptions"></v-select>
        <label v-if="categoryError !== ''" class="error-label">{{categoryError}}</label>
      </div>
      <div class="buttonContainer">
        <va-button class="btn alignleft" @click="cancel">CANCEL</va-button>
        <va-button class="btn alignright" @click="save">SAVE</va-button>
      </div>
      
    </div>
  </va-card>
</template>

<script>
import { mapState, mapActions } from "vuex";
import vSelect from 'vue-select';
import 'vue-select/dist/vue-select.css';

export default {
  name: "edit-report-modal",
  props: {
    title: String,
    propsId: {type:Number, default: 0},
    propsName: {type:String, default: ""},
    propsWorkspaceId: {type:String, default: ""},
    propsReportId: {type:String, default: ""},
    propsPermissionId:{type:Number, default:0},
    propsCategoryId:{type:Number, default:0}
  },
  components:{
    vSelect
  },
  data() {
    return {
      id: 0,
      name: "",
      workspaceId: "",
      reportId: "",
      permissionId:0,
      categoryId:0,
      nameError: "",
      workspaceIdError:"",
      reportIdError:"",
      permissionError:"",
      categoryError:"",
      permission: null,
      category: null
    };
  },
  created() {
    this.id = this.propsId;
    this.name = this.propsName;
    this.workspaceId = this.propsWorkspaceId;
    this.reportId = this.propsReportId;
    this.permissionId = this.propsPermissionId;
    this.categoryId = this.propsCategoryId;

    if(this.permissionId !== 0 && this.permissionOptions){
      this.permission = this.permissionOptions.find(p => p.id === this.permissionId)
    }
    if(this.categoryId !== 0 && this.categoryOptions){
      this.category = this.categoryOptions.find(c => c.id === this.categoryId)
    }
  },
  computed: {
    ...mapState({
      permissionOptions: state => state.admin.adminReportList ? state.admin.adminReportList.permissions : [],
      categoryOptions: state => state.admin.adminReportList ? state.admin.adminReportList.reportCategories : [],
      selectedEntity: state => state.user.selectedEntity
    })
  },
  methods: {
    ...mapActions({
      addNewReport: "admin/addNewReport",
      updateReport: "admin/updateReport",
      getReportList: "report/getReportList"
    }),

    cancel() {
      this.$emit("close");
    },
    save() {
        if(this.validateInput()){
            var param = {
                name: this.name,
                workspaceId: this.workspaceId,
                reportId: this.reportId,
                entityId: this.selectedEntity ? this.selectedEntity.id : 0,
                permissionId: this.permission.id,
                categoryId: this.category.id
            };

            if(this.id && this.id > 0){
              param.id = this.id
                this.updateReport(param)
                .then(() => {
                  if(this.selectedEntity){
                    this.getReportList(this.selectedEntity.id)
                  }
                })
                .finally(()=>{this.$emit("close");});
            }
            else{
                this.addNewReport(param)
                .then(() => {
                  if(this.selectedEntity){
                    this.getReportList(this.selectedEntity.id)
                  }
                })
                .finally(()=>{this.$emit("close");});
            }
            
        }
    },
    validateInput(){
        let isValid = true;
        var name_regex = new RegExp("^[-_ a-zA-Z0-9]+$");
        var id_regex   = new RegExp("^[-_ a-zA-Z0-9]+$")

        if(this.name === ''){
            this.nameError = 'Required';
            isValid = false;
        }
        else if( ! name_regex.test(this.name) ){
            this.nameError='Only allow alphabet, numbers, space and dash';
            isValid = false;            
        }        
        else{
            this.nameError = '';
        }
        
        if(this.workspaceId === ''){
            this.workspaceIdError = 'Required';
            isValid = false;
        }
        else if( ! id_regex.test(this.workspaceId) ){
            this.workspaceIdError='Only allow alphabet, numbers, space and dash';
            isValid = false;            
        }                
        else{
            this.workspaceIdError = '';
        }

        if(this.reportId === ''){
            this.reportIdError = 'Required';
            isValid = false;
        }
        else if( ! id_regex.test(this.reportId) ){
            this.reportIdError='Only allow alphabet, numbers, space and dash';
            isValid = false;            
        }                     
        else{
            this.reportIdError = '';
        }

        if(this.permission){
          this.permissionError = '';
        }
        else{
          this.permissionError = 'Required';
            isValid = false;
        }

        if(this.category){
          this.categoryError = '';
        }
        else{
          this.categoryError = 'Required';
            isValid = false;
        }

        return isValid;
    }
  }
};
</script>

<style lang='scss' scoped>
.container {
  box-shadow: none !important;

  & .body {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;

    & .inputSection {
      //display: contents;

      & .readonly-input {
        padding-left: 0.75rem;
      }

      & .form-label {
        font-weight: 600;
        display: block;
      }

      & .form-input {
        border: 1px solid rgba(60, 60, 60, 0.26);
        border-radius: 4px;
        height: 2rem;
        max-height: 2rem;
        width: 100%;
        color: #333333;

        &.hasError {
          border-color: #d43d27;
        }
      }

      & + .inputSection {
        margin-top: 0.75rem;
      }

      & .error-label {
        font-size: 0.75rem;
        color: #d43d27;
        font-weight: bold;
        margin-left: 0.25rem;
      }
    }

    & .buttonContainer {
      margin-top: 0.75rem;
    }
  }
}

.alignright {
  float: right;
}

.alignleft {
  float: left;
}
</style>

<style lang="scss">
.v-select.hasError {
  & > .vs__dropdown-toggle {
    border-color: #d43d27;
  }
}
</style>