import Benchmark from './views/benchmark-report'

const benchmarkReportRoutes = [
    {
        path: 'benchmark_report',
        name: 'benchmark_report',
        component: Benchmark,
        meta: {
        breadcrumb: [
            { name: 'BENCHMARK REPORT' }
        ]
        }
    }
]

export default benchmarkReportRoutes
