import store from '../../app-state';

/**
 * @description Represents functionality for user permission
 */
class PermissionService {

    constructor () {

    }

    /**
     * @description Function to check whether user has given permission
     */
    hasPermission (permission) {
        const userInfo = store.state.user;
        if(userInfo.authenticated === false)
            return false;
        
        if(!userInfo.specialPermissionList.includes(permission)){
            //if user doesn't have special permission check permission for current selected entity
            const selectedEntity = store.state.user.selectedEntity;
            if(selectedEntity)
            {
                const permissions = userInfo.permissionList[selectedEntity.id];
                if(permissions.includes(permission)){
                    return true;
                }
                else{
                    return false;
                }
            }
            else{
                return false;
            }
        }
        else{
            return true;
        }
    }

    /**
     * @description Function to check whether user has permission to view given report
     */
    hasReportPermission (to){
        let result = false;
        const availableReports = store.state.report.availableReports;
        const codenameFromRoute = to.params ? to.params.codename : '';

        
        let allReports = []
        Object.keys(availableReports).forEach(cate => {
            allReports = [...allReports, ...availableReports[cate]]
        });

        for (let index = 0; index < allReports.length; index++) {
            const report = allReports[index];
            if(report.codename === codenameFromRoute){
                result = true;
                break;
            }
        }

        return result;
    }
}

export const permissionService = new PermissionService()
