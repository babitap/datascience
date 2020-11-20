<template>
  <div class="profile app-navbar-actions">
    <span class="profile-name" @click="showHideProfileDropDown">{{userName}}</span>
    <profile-dropdown class="app-navbar-actions__item app-navbar-actions__item--profile" v-if="showProfileDropDown" @closeMe="hideDropDown">
    </profile-dropdown>
  </div>
</template>

<script>
import ProfileDropdown from './dropdowns/profile-dropdown'

export default {
  name: 'app-navbar-actions',
  components: {
    ProfileDropdown,
  },
  data () {
    return {
      showProfileDropDown: false,
    }
  },
  props: {
    userName: {
      type: String,
      default: '',
    },
  },
  methods: {
    showHideProfileDropDown(){
        this.showProfileDropDown = !this.showProfileDropDown
      },
    hideDropDown(){
      this.showProfileDropDown = false;
    },
    close (e) {
      if (!this.$el.contains(e.target)) {
        this.showProfileDropDown = false;
      }
    },
  },
  mounted () {
    document.addEventListener('click', this.close)
  },
  beforeDestroy () {
    document.removeEventListener('click',this.close)
  },
}
</script>

<style lang="scss">
.app-navbar-actions {
  display: flex;

  &__item {
    margin-top: 0.3rem;
    padding: 0;
    margin-left: 1.25rem;
    margin-right: 1.25rem;

    &:last-of-type {
      margin-right: 0;
    }

    &--profile {
      display: flex;
      justify-content: center;
      margin: auto 0 auto 1.25rem;
    }

    @include media-breakpoint-down(lg) {
      margin-right: 0.25rem;
    }

    @include media-breakpoint-down(sm) {
      margin-right: 0;

      &:first-of-type {
        margin-left: 0;
      }

      &--profile {
        position: absolute;
        right: 0.75rem;
        top: 1.25rem;
        height: fit-content;
        margin: auto;
      }
    }
  }
}
</style>
<style scoped>
.profile {
  background-color: #d43d3d;
  border-radius: 50%;
  display: inline-block;
  color: white;
  font-size: 1rem;
  line-height: 1.5;
  font-weight: 700;
  width: 3rem;
  height: 3rem;
  position: relative;
  cursor: pointer;
}

.profile-name {
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}
</style>
