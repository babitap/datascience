<template>
  <div class="app-navbar-school__center lg5 md4" v-if="entity">
    <span
      class="app-navbar-school__text"
      :style="{color: this.$themes.gray}"
    >
      {{ entity.entity_name }} &nbsp;
    </span>
    <va-button
      @click="clickSelectSchool"
      class="app-navbar-school__button_select"
    >
      SWITCH
    </va-button>

  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'app-navbar-school',
  data () {
    return {
      toastText: 'Unexpected error while retrieving list of schools',
      toastDuration: 2500,
      // toastIcon: 'fa-star-o',
      toastPosition: 'top-center',
      isToastFullWidth: false,
    }
  },
  async created () {
    //this.setSchool({'ACARA_ID':48004, 'School_Name':'The Cathedral School of St Anne and St James'}); 
    //await this.getSelectedSchool(0)
    //await this.getSchools()
  },
  computed: {
    ...mapState({
      entity: state => state.user.selectedEntity,
    }),
  },
  methods: {
    ...mapActions({
      //getSchools: 'schools/getSchools',
      setSchool: 'schools/setSelectedSchool',
      getSelectedSchool: 'schools/getSelectedSchool',
    }),
    clickSelectSchool () {
      this.$router.push({ name: 'school-list' })
        // eslint-disable-next-line handle-callback-err
        .catch(err => {})
    },
  },
}

</script>

<style lang="scss">

.app-navbar-school {
  &__center {
    display: flex;
    margin-left: 3rem;
    justify-content: space-between;
    align-items: center;
  }

  @include media-breakpoint-down(md) {
    &__center {
      display: none !important;
    }
  }

  &__text {
    color: $lighter-gray;
  }

  &__mailto-link:hover {
    filter: brightness(85%);
  }

  &__button {
    width: auto;
    margin: 0 0 0 1rem !important;
    font-weight: bold;

    .va-button__content__icon-left.fa-github {
      font-size: 1.5rem;
    }
  }

  @include media-breakpoint-down(lg) {
    &__button {
      display: none !important;
    }
  }
}
</style>
