<template>
        
      <div id="app" class="app">
      <div v-if="showLoading" id="loading">
          <LoadingAnimation/>
      </div>
      <router-view v-bind:class="{ noClick: showLoading }" />
  </div>
  
</template>

<script>
import { mapState, mapActions } from 'vuex'
import LoadingAnimation from "../app/modules/shared/LoadingAnimation"

export default {
  name: 'app',
  components: {
      LoadingAnimation
  },
  data () {
    return {
      // Temporary config for 2.1.
      contextConfig: {
        gradient: true,
        shadow: 'lg', // 3 states: 'sm', 'lg', undefined (no shadow).
        invertedColor: false,
      },
    }
  },
  provide () {
    return {
      contextConfig: this.contextConfig,
    }
  },
  methods: {
    ...mapActions({
      dismissError: 'dismissError',
    }),
  },
  computed: mapState(['error', 'showLoading']),
  watch: {
    // Temporary colors fix for 2.1.
    'contextConfig.invertedColor' (val) {
      const invertedColorClass = 'va-inverted-color'
      if (val) {
        document.body.classList.add(invertedColorClass)
      } else {
        document.body.classList.remove(invertedColorClass)
      }
    },
    error (newValue, oldValue) {
      if (newValue) {
        this.showToast(newValue, {
          position: 'top-center',
          duration: 2500,
          onComplete: () => {
            this.dismissError()
          },
        })
      }
    },
  },
}
</script>

<style lang="scss">
@import '../sass/main.scss';

body {
  height: 100%;

  #app {
    height: 100%;
  }
}

#loading {
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  position: fixed;
  opacity: 0.3;
  background-color: #ffffff;
  z-index: 9999;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.noClick {
  pointer-events: none;
}
</style>
