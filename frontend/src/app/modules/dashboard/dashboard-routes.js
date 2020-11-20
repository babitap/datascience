import Dashboard from './views/dashboard'
import TestPage from './views/testpage'

const dashboardRoutes = [
  {
    path: 'dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: {
      breadcrumb: [
        { name: '' }
      ]
    }
  },
  {
    path: 'testpage',
    name: 'testpage',
    component: TestPage,
    meta: {
      breadcrumb: [
        { name: 'TEST PAGE' }
      ]
    }
  },
]

export default dashboardRoutes
