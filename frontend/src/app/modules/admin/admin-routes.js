import Admin from './views/admin'

const adminRoutes = [
    {
        path: 'admin',
        name: 'admin',
        component: Admin,
        meta: {
        breadcrumb: [
            { name: 'Permission Admin' }
        ],
        requiresPermission: 'user_management'
        }
    }
]

export default adminRoutes
