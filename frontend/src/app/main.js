// Polyfills
import 'core-js/stable'
import 'regenerator-runtime/runtime'
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './app'
import { ColorThemePlugin } from '../services/vuestic-ui'
import store from './app-state'
import router from './app-routes'
import { VuesticPlugin } from '../services/vuestic-ui/components'
import VueClipboard from 'vue-clipboard2'

/* ----------------------------------------------------------------------------- */
/* enable plotly module  and other components, will be moved to separated folder */
import { Plotly } from 'vue-plotly'
Vue.component('plotly', Plotly );

import VModal from 'vue-js-modal'
Vue.use(VModal, { dialog: true , dynamic: true, dynamicDefaults: { clickToClose: false } })

// enable self-made componnets 
import BarChartSimple from './modules/shared/BarChartSimplePlotly.vue';
Vue.component('bar-chart-simple', BarChartSimple )


import BreadCrumbs from './modules/shared/BreadCrumbs.vue';
Vue.component('breadcrumbs', BreadCrumbs)


//import { vuetable } from 'vuetable-2'
//Vue.component('vuetable', vuetable);

/*import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify)


import VuetifyDraggableTreeview from 'vuetify-draggable-treeview'
Vue.use(VuetifyDraggableTreeview)*/

/* ----------------------------------------------------------------------------- */

//import '../metrics'

if (process.env.VUE_APP_BUILD_VERSION) {
  // eslint-disable-next-line
  const message = `%c${'Build_information:'}\n %c${'Version'}: %c${VERSION},\n %c${'Timestamp'}: %c${TIMESTAMP},\n %c${'Commit'}: %c${COMMIT}`
  // eslint-disable-next-line
  console.info(
    message,
    'color: blue;', 'color: red;', 'color: blue;', 'color: red;', 'color: blue;', 'color: red;', 'color: blue;',
  )
}


Vue.use(VuesticPlugin)
Vue.use(VueClipboard)

Vue.use(ColorThemePlugin, {
  // override colors here.
})

// router.beforeEach((to, from, next) => {
//   store.commit('setLoading', true)
//   next()
// })

// router.afterEach((to, from) => {
//   store.commit('setLoading', false)
// })

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  beforeCreate () {
    this.$store.dispatch('user/init')
  },
  render: h => h(App),
})
