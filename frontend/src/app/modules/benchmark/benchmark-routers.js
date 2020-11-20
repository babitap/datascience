import Benchmark from './views/benchmark'

const benchmarkRoutes = [
    {
        path: 'benchmark',
        name: 'benchmark',
        component: Benchmark,
        meta: {
        breadcrumb: [
            { name: 'BENCHMARK' }
        ]
        }
    }
]

export default benchmarkRoutes
