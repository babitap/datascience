<template>
  <va-card class="container" style="overflow-x: auto; overflow-y: visible;">
    <p class="display-5" style="color: #5f6e78;">{{title}}</p>

    <div class="body">
      <div class="inputSection">
      <!--
        <va-input
          v-model="user_group_name"
          label="New Group Name"
          placeholder="Enter group name here"
        />
        -->
        <label class="flex xs12 form-label">Group Name</label>
        <input class="flex xs12 form-input" v-bind:class="{ hasError: nameError !== '' }" v-model="user_group_name" placeholder="Enter group name here">        
        <label v-if="nameError !== ''" class="error-label">{{nameError}}</label>
      </div>
      <div class="inputSection">
      <!--
        <va-input
          v-model="user_group_description"
          label="New Group Description"
          type="textarea"
          placeholder="Enter group description here"
        />
        -->
        <label class="flex xs12 form-label">Group Description</label>
        <input class="flex xs12 form-input" v-bind:class="{ hasError: descriptionError !== '' }" v-model="user_group_description" placeholder="Enter group description here">         
        <label v-if="descriptionError !== ''" class="error-label">{{descriptionError}}</label>
      </div>
      <div class="buttonContainer">
        <va-button class="btn alignleft" @click="cancel">CANCEL</va-button>
        <va-button class="btn alignright" @click="save">SAVE</va-button>
      </div>
      <!--
      <va-button class="btn alignleft" @click="cancel">CANCEL</va-button>
      <va-button
        class="btn alignright"
        @click="save"
      >SAVE</va-button>
      -->
    </div>
  </va-card>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "add-group-modal",
  props: {
    title: String,

    industry_id: { type: Number },
    entity_id: { type: Number },

    usergroup_id: { type: Number, default: null },
    usergroup_name: { type: String, default: "" },
    usergroup_description: { type: String, default: "" }
  },
  data() {
    return {
      user_group_id: null,
      user_group_name: "",
      user_group_description: "",
      nameError: "",
      descriptionError: ""
    };
  },
  created() {
    this.user_group_id = this.usergroup_id;
    this.user_group_name = this.usergroup_name;
    this.user_group_description = this.usergroup_description;
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
      loadAdminTreeJsonData: "admin/getAdminTreeJsonData",
      addNewUserGroup: "admin/addNewUserGroup",
      editUserGroup: "admin/editUserGroup",
      loadAdminUserGroupJsonData: "admin/getAdminUserGroupJsonData"
    }),

    cancel() {
      this.$emit("close");
    },
    save() {
        var isValid = true 
        var name_regex = new RegExp("^[a-zA-Z ]+$");
        var description_regex = new RegExp("^[-_ a-zA-Z0-9]+$")

        if(this.user_group_name === ""){
            console.log('new group name is empty')
            this.nameError = 'Required' ;
            isValid = false 
        }
        else if( ! name_regex.test(this.user_group_name) ){
            this.nameError = 'Only allow alphabet and space' ;
            isValid = false;            
        }
        else {
            this.nameError = ""
        }

        if( ! description_regex.test(this.user_group_description) ){
            this.descriptionError = 'Only allow alphabet, numbers, space and dash' ;
            isValid = false;            
        }
        else {
            this.descriptionError = ""
        }

        if(isValid){
            var param = {
                industry_id: this.industry_id,
                entity_id: this.entity_id,
                usergroup_id: this.usergroup_id,
                usergroup_name: this.user_group_name,
                usergroup_description: this.user_group_description
            };

            if(this.usergroup_id && this.usergroup_id > 0){
                this.editUserGroup(param);
            }
            else{
                this.addNewUserGroup(param);
            }
            this.$emit("close");
        }
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