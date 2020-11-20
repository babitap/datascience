<template>
    <div class="permission-denied">
        <div class="container">
            <img class="denied-img" src="../../../../assets/img/permission_denied.svg" alt="Permission Denied">
            <h1 class="warning-title">OOOH! PERMISSION DENIED</h1>
            <div class="content-container">
                <p class="content">Sorry about that, but you don't have permission to access this page.</p>
            </div>
            <div class="button-container">
                <va-button class="btn" @click="navigateToDashboard">TAKE ME TO DASHBOARD</va-button>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: "permission-denied",
    components: {
    },
  data() {
    return {
    }
  },
  computed: {
  },
  watch:{
  },
  methods: {
    navigateToDashboard(){
        this.$router.push({ name: "dashboard" });
    }
  }
}
</script>
<style scoped>
.permission-denied {
  text-align: center;
}

.container {
  display: inline-block;
  width: 80%;
}

.denied-img {
  width: 30%;
  height: 30%;
}

.warning-title {
  margin-top: 2rem;
  font-size: xx-large;
}

.content-container {
  text-align: center;
}

.content {
  width: 30%;
  display: inline-block;
  font-size: large;
  margin-top: 2rem;
}

.button-container {
  margin-top: 2rem;
}
</style>

