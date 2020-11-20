import Vue from 'vue'
import Vuex from 'vuex'

import { userState as UserModule } from './shared/state/user-data'
import { schoolsState as SchoolsModule } from './modules/schools/schools-data'
import { dashboardState as DashboardModule } from './modules/dashboard/dashboard-data'
import { benchmarkState as BenchmarkModule } from './modules/benchmark/benchmark-data'
import { benchmarkReportState as BenchmarkReportModule } from './modules/benchmark-report/benchmark-report-data'
import { adminState as AdminModule } from './modules/admin/admin-data'
import { mapState as MapModule } from './modules/map/map-data'
import { reportState as ReportModule } from './modules/report/report-data'

Vue.use(Vuex)

export default new Vuex.Store({
  strict: false,
  state: {
    error: null,
    showLoading: false
  },
  mutations: {
    setError (state, error) {
      state.error = error
    },
    setShowLoading(state) {
        state.showLoading = !state.showLoading;
    }
  },
  actions: {
    raiseError (context, error) {
      context.commit('setError', error)
    },
    dismissError (context) {
      context.commit('setError', null)
    },
    showLoadingAnimation(context, show) {
        if(show !== this.showLoading){
            context.commit('setShowLoading')
        }
    }
  },
  modules: {
    user: UserModule,
    schools: SchoolsModule,
    dashboard: DashboardModule,
    benchmark: BenchmarkModule,
    benchmarkReport: BenchmarkReportModule,
    admin: AdminModule,
    report: ReportModule,
    map: MapModule
  },
})
