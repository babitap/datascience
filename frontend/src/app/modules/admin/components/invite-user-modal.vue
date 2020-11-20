<template>
  <va-card class="container" style="overflow-x: auto; overflow-y: visible;">
    <p class="display-5" style="color: #5f6e78;">{{title}}</p>

    <div class="body">
        <div>
            <label class="form-label">Email</label>
            <input class="email-input" v-model="email" placeholder="Enter email address here">
            <label v-if="emailError === true" class="error-label">Please enter email</label>
        </div>
        <div class="form-container select-container">
            <label class="form-label">Select one or more schools for user</label>
            <v-select class="selection" multiple label="name" v-model="entities" :options="options"></v-select>
            <label v-if="selectionError === true" class="error-label">Please select at least one school</label>
        </div>
        <div class="flex xs12 form-container button-container">
            <div class="alignleft">
                <va-button class="btn" @click="cancel">CANCEL</va-button>
            </div>
            <div class="alignright">
                <va-button class="btn" @click="save">INVITE</va-button>
            </div>
        </div>
        <div class="flex xs12 form-container error-container">
            <label v-if="apiError !== ''" class="error-label alignright">{{apiError}}</label>
        </div>
    </div>
  </va-card>
</template>

<script>
import { mapState, mapActions } from "vuex";
import vSelect from 'vue-select';
import 'vue-select/dist/vue-select.css';

export default {
  name: "invite-user-modal",
  components:{
      vSelect
  },
  props: {
    title: {
        type: String,
        required: false,
        note:"Title for the multiple selection"
    },
    options: {
      type: Array,
      required: false,
      default: () => [],
      note: "Options of dropdown. An array of options with id and name"
    },
    selectedEntity:{
        type: Number,
        required: false,
        note:"Current selected entity"
    }
  },
  data() {
    return {
      email: "",
      entities: [],
      emailError: false,
      selectionError: false,
      apiError: ""
    };
  },
  created() {
      if (!this.entities.some(e => e.id === this.selectedEntity))
      {
          this.entities.push(this.options.find(option => option.id === this.selectedEntity));
      }
  },
  computed: {
  },

  methods: {
    ...mapActions({
        invitNewUser: "admin/invitNewUser"
    }),

    cancel() {
      this.$emit("close");
    },
    save() {
        this.emailError = false;
        this.selectionError = false;
        this.apiError = "";

      if(this.email === ""){
          this.emailError = true;
      }
      if(this.entities.length === 0){
          this.selectionError = true;
      }
      if (this.emailError === false && this.selectionError === false) {
        this.invitNewUser({email:this.email, entities:this.entities.map(e => e.id), selectedEntity:this.selectedEntity})
            .then(res => {
                if(res.success == true){
                    this.$emit("close");
                }
                else{
                    this.apiError = res.errorMessage;
                }
            })
            .catch(err => {
                this.apiError = "Error sending invite request";
            })
            .finally(()=>{
                //stop loading animation
            });
      }
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

.selection {
  margin-top: 0.25rem;
}

.form-label {
  font-size: 1rem;
  color: #34495e;
  width: 100%;
}

.email-input {
  width: 100%;
  border-color: rgba(60, 60, 60, 0.26);
  border-width: thin;
  border-radius: 4px;
  height: 2rem;
}

.error-label {
  font-size: 0.75rem;
  color: #d43d27;
  font-weight: bold;
  margin-left: 0.25rem;
}

.form-container {
  margin-top: 0.75rem;
}

.select-container {
  height: 4rem;
}

.button-container {
  height: 3rem;
}

.error-container {
  height: 1rem;
}
</style>