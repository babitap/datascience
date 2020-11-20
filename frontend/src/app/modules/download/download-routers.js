import DownloadFinance from './views/download-finance'
import DownloadEnrolment from './views/download-enrolment'

const downloadRoutes = [
    {
        path: 'download_finance',
        name: 'download_finance',
        component: DownloadFinance,
        meta: {
        breadcrumb: [
            { name: 'Download Financial Documents' }
        ]
        }
    },
    {
        path: 'download_enrolment',
        name: 'download_enrolment',
        component: DownloadEnrolment,
        meta: {
        breadcrumb: [
            { name: 'Download Enrolment Documents' }
        ]
        }
    }    
]

export default downloadRoutes
