import PermissionDenied from './views/permission-denied'

const permissionDeniedRoutes = [
    {
        path: 'permission-denied',
        name: 'permission-denied',
        component: PermissionDenied,
        meta: {
            breadcrumb: [
                { name: '' }
            ]
        }
    }
]

export default permissionDeniedRoutes