import store from '../../app-state';

/**
 * @description Global servie to show/hide loading animation
 */
class LoadingService {

    constructor () {

    }

    /**
     * @description Function to show/hide loading animation
     */
    showLoading (toShow) {
        store.dispatch('showLoadingAnimation', toShow);
    }
}

export const loadingService = new LoadingService()
