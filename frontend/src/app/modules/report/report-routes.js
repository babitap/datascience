import Report from './views/report'

const reportRoutes = [
    {
        path: 'report/:codename',
        name: 'report',
        component: Report,
        props: true,
        meta: {
            breadcrumb: [
                { name: 'Report' }
          ],
            requiresReportPermission: true
        }
    },
    {
        path: 'report',
        redirect: { name: 'dashboard' },
        name: 'report',
        component: Report,
        meta: {
            breadcrumb: [
                { name: 'Report' }
            ]
        }
    }
]

export default reportRoutes
