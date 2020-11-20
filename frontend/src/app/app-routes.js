import Vue from 'vue'
import VueRouter from 'vue-router'
import landingRoutes from './modules/landing/landing-routes'
import schoolRoutes from './modules/schools/schools-routes'
import AppLayout from './layouts/portal/app-layout'
import store from './app-state'
import { permissionService } from '@/app/shared/services/permission-service';

import dashboardRoutes from './modules/dashboard/dashboard-routes'
import benchmarkRoutes from './modules/benchmark/benchmark-routers'
import benchmarkReportRoutes from './modules/benchmark-report/benchmark-report-routers'
import adminRoutes from './modules/admin/admin-routes'
import mapRoutes from './modules/map/map-routers'
import permissionDeniedRoutes from './modules/permission-denied/permission-denied-routes'
import reportRoutes from './modules/report/report-routes'
import downloadRoutes from './modules/download/download-routers'

Vue.use(VueRouter)

const appRoutes = [
  {
    path: '/',
    redirect: '/home',
  },
  {
    name: 'portal',
    path: '/portal',
    component: AppLayout,
    meta: {
      requiresAuth: true,
    },
    children: [...dashboardRoutes, ...schoolRoutes, ...benchmarkRoutes, ...benchmarkReportRoutes, ...adminRoutes, ...mapRoutes, ...permissionDeniedRoutes, ...reportRoutes, 
      ...downloadRoutes
    ],
  },
]

const routes = [...appRoutes, ...landingRoutes]

const router = new VueRouter({
  mode: 'history',
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const user = JSON.parse(localStorage.getItem('user'))
    if (user && user.authenticated && user.jwt) {
        //Now check permission
        const rp = to.meta.requiresPermission;
        const rrp = to.meta.requiresReportPermission;
        if(rp){
            if(true === permissionService.hasPermission(rp)){
                next();
            }
            else{
                next('/portal/permission-denied');
            }
        }
        else if(rrp){
            if(true === permissionService.hasReportPermission(to)){
                next();
            }
            else{
                next('/portal/permission-denied');
            }
        }
        else{
            next()
        }
      
    } else {
      next('/')
    }
  } else {
    next()
  }
})

export default router
