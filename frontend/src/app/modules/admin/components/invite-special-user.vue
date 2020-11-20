<template>
  <div class="flex container">
        <p class="flex xs12 group-title"></p>
            <div class="flex xs12 content">
                <div class="emailSection">
                    <label class="flex xs12 form-label">Email</label>
                    <input class="flex xs12 email-input" v-model="email" placeholder="Enter email address here">
                    <label v-if="emailError === true" class="error-label">Please enter email</label>
                </div>
                <div class="flex xs12 checkboxSection">
                    <div class="buttons">
                        <va-radio-button
                        v-model="selectedRole"
                        option="1"
                        label="Super User"
                    />
                    <va-radio-button
                        v-model="selectedRole"
                        option="2"
                        label="Findex User"
                    />
                    <va-radio-button
                        v-model="selectedRole"
                        option="3"
                        label="Findex All User"
                    />
                    </div>
                    <label v-if="selectionError === true" class="error-label">Please select at least one role</label>
                </div>
                
                <div class="flex xs12 form-container button-container">
                    <div class="alignright">
                        <va-button class="btn" @click="save">INVITE</va-button>
                    </div>
                </div>
                <div v-if="apiError !== ''" class="flex xs12 form-container error-container">
                    <label class="error-label">{{apiError}}</label>
                </div>
                <div v-if="apiSuccess !== ''" class="flex xs12 form-container error-container">
                    <label class="success-label">{{apiSuccess}}</label>
                </div>
            </div>
    </div>
</template>
<script>
import { mapActions } from "vuex";
export default {
    name: "invite-special-user",
  components:{
      
  },
  props: {
  },
  data() {
    return {
      email: "",
      selectedRole: '',
      emailError: false,
      selectionError: false,
      apiError: "",
      apiSuccess:""
    };
  },
  methods: {
    ...mapActions({
        invitNewUser: "admin/invitNewUser"
    }),

    save() {
        this.emailError = false;
        this.selectionError = false;
        this.apiError = "";
        this.apiSuccess = ""

      if(this.email === ""){
          this.emailError = true;
      }
      if(this.selectedRole === ''){
          this.selectionError = true;
      }
      if (this.emailError === false && this.selectionError === false) {
            let user = {
                email:this.email
            }
            if(this.selectedRole === '1'){
                user.superUser = true;
            }
            else if(this.selectedRole === '2'){
                user.findexUser = true;
            }
            else if(this.selectedRole === '3'){
                user.findexAllUser = true;
            }
        this.invitNewUser(user)
            .then(res => {
                if(res.success == true){
                    this.apiSuccess = "Invitation was sent successfully";
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
                this.email = '';
                this.selectedRole = '';
            });
      }
    }
  }
}
</script>

<style scoped>
.container {
  border: none;
  border-radius: 0.375rem;
  background: white;
  display: flex;
  flex-wrap: wrap;
  min-width: 593px;
  max-width: 50%;
}

.group-title {
  float: left;
  font-weight: 600;
  padding: 0 !important;
  width: 100%;
}

.emailSection {
  margin-top: 5px;
  margin-left: 5px;
}

.content {
  margin-top: 5px;
}

.form-label {
  font-size: 1rem;
  color: #34495e;
  display: block;
  font-weight: 600;
}

.email-input {
  width: 100%;
  border-color: rgba(60, 60, 60, 0.26);
  border-width: thin;
  border-radius: 4px;
  height: 2rem;
  padding-left: 5px;
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
  text-align: right;
}

.button-container {
  padding-right: 0 !important;
}

.buttons {
  display: flex;
  width: 100%;
  justify-content: space-between;
}

.checkboxSection {
  padding-left: 0.25rem !important;
}

.error-container {
  display: flex;
}

.error-container > label {
  text-align: right;
}
</style>