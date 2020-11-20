<template>
  <nav
    class="app-navbar"
    :style="navbarStyle"
  >
    <div class="app-navbar__content row">
      <div class="app-navbar__menu-container">
        <va-icon-menu
          class="app-navbar__menu"
          v-if="!minimized && !isTopBar"
          @click.native="$emit('update:minimized', !minimized)"
          :color="contextConfig.invertedColor ? $themes.gray : 'white'"
        />

        <va-icon-menu-collapsed
          class="app-navbar__menu"
          v-if="minimized && !isTopBar"
          @click.native="$emit('update:minimized', !minimized)"
          :color="contextConfig.invertedColor ? $themes.gray : 'white'"
        />

        <router-link
          class=""
          to="/"
        >
          <img src="@/assets/img/findex_logo_white_dash.png" height="31"/>
        </router-link>
      </div>

      <app-navbar-school />

      <app-navbar-actions
        class="app-navbar__actions md5 lg4"
        :user-name="getUserInitial"
        :is-top-bar.sync="isTopBarProxy"
      />
    </div>
    <div
      class="app-navbar__shape"
      :style="shapeStyle"
    ></div>
  </nav>
</template>

<script>
import VaIconMenu from '@/iconset/VaIconMenu'
import VaIconMenuCollapsed from '@/iconset/VaIconMenuCollapsed'
import AppNavbarActions from './components/app-navbar-actions'
import AppNavbarSchool from './components/app-navbar-school'
import { colorShiftHsl, ColorThemeMixin } from '@/services/vuestic-ui'
import { mapState, mapActions, mapGetters } from 'vuex'

export default {
  name: 'app-navbar',
  mixins: [ColorThemeMixin],
  inject: ['contextConfig'],
  components: {
    VaIconMenu,
    VaIconMenuCollapsed,
    AppNavbarActions,
    AppNavbarSchool,
  },

  props: {
    isTopBar: {
      type: Boolean,
      required: true,
    },
    minimized: {
      type: Boolean,
      required: true,
    },
  },
  data () {
    return {
      userName: 'Fred G.',
    }
  },
  async created(){
    if(  this.schools.length == 0 ){
      this.getSchools();  // school list will be looked after in get user profile
    }
  },
  computed: {
    ...mapGetters("user", ["getUserInitial"]),
    ...mapState({
      schools: state => state.schools.schools,
    }),
    isTopBarProxy: {
      get () {
        return this.isTopBar
      },
      set (isTopBar) {
        this.$emit('update:isTopBar', isTopBar)
      },
    },
    minimizedProxy: {
      get () {
        return this.minimized
      },
      set (minimized) {
        this.$emit('update:minimized', minimized)
      },
    },
    navbarStyle () {
      const style = {
        backgroundColor: this.$themes.dark,
      }

      if (this.contextConfig.gradient) {
        style.backgroundColor = colorShiftHsl(this.$themes.secondary, {
          s: -13,
          l: 15,
        }).css
      }

      if (this.contextConfig.shadow === 'sm') {
        style.boxShadow = !this.isTopBar ? '0 2px 3px 0 rgba(52, 56, 85, 0.25)' : null
      }
      return style
    },

    shapeStyle () {
      return {
        borderTopColor: this.contextConfig.gradient ? colorShiftHsl(this.$themes.secondary, {
          h: -1,
          s: -11,
          l: 10,
        }).css : 'transparent',
      }
    },
  },
  methods:{
    ...mapActions({
      getSchools: 'schools/getSchools',
    }),
  },
}
</script>

<style lang="scss">
$nav-border-side-width: 3.1875rem;

.app-navbar {
  transition: background-color 0.3s ease; /* sidebar's bg color transitions as well -> consistency */
  display: flex;
  padding: 1rem 1rem;
  z-index: 1;

  &__content {
    z-index: 1;
    align-items: center;
    justify-content: space-between;
    flex-direction: row;
    flex-wrap: wrap;
    height: 100%;
    flex: 1 1 auto;
  }

  &__menu {
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1rem;
    margin-right: 1.5rem;
  }

  &__menu-container {
    display: flex;
    flex-wrap: nowrap;
    height: 1.5rem;
  }

  &__actions {
    justify-content: flex-end;
  }

  &__shape {
    transition: border-top-color 0.3s ease; /* sidebar's bg color transitions as well -> consistency */
    width: 33%;
    max-width: 467px;
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    margin: auto;
    border-top: 4.215rem solid transparent; // hardcoded size
    border-left: $nav-border-side-width solid transparent;
    border-right: $nav-border-side-width solid transparent;
    height: 0;
  }

  @include media-breakpoint-down(sm) {
    &__content {
      align-items: flex-end;
    }

    &__actions {
      margin-top: 1.25rem;
      justify-content: space-between;
      width: 100%;
    }

    &__shape {
      display: none;
    }
  }
}
</style>
