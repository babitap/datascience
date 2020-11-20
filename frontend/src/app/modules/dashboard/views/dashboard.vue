<template>
  <div class="dashboard">


    <EducationDashboard v-if="selectedEntity && selectedEntity.industry_name && selectedEntity.industry_name.toLowerCase() === 'education'" />


    <router-link v-else-if="selectedEntity && selectedEntity.industry_name && selectedEntity.entity_name.toLowerCase() === 'key research'" class=""
                 to="/">
      <img src="@/assets/img/NZ_Farms_Minified_Text_3_logo.jpg" width="100%" />
    </router-link>

    <router-link v-else-if="selectedEntity && selectedEntity.industry_name && selectedEntity.entity_name.toLowerCase() === 'altra motion'" class=""
                 to="/">
      <img src="@/assets/img/Altra_Motion_homepage.jpg" width="100%" />
    </router-link>

  </div>

  
  

</template>

<script>
import { mapState, mapActions } from "vuex";
import EducationDashboard from "../components/education-dashboard"

export default {
  name: "dashboard",
  components: {
        EducationDashboard
    },
  data() {
    return {
    };
  },

  computed: {
    ...mapState({
      selectedEntity: state => state.user.selectedEntity
    })
  },
  methods: {
  },
  watch: {  
  }
};
</script>
