import { createStore } from 'vuex';

export default createStore({
    state: {
        modalState: {
            isOpen: false,
        },
        signupFormState: {
            isOpen: false,
        }
    },
    getters: {
        getModalState(state) {
            console.log("getModalState from store");
            return state.modalState.isOpen;
        },
        getSignupFormState(state) {
            return state.signupFormState.isOpen;
        }
    },
    mutations: {
        toggleModalState: function(state, status) {
            console.log("toggelModalState to store");
            state.modalState.isOpen = status;
        },
        toggleSignupFormState: function(state, status) {
            state.signupFormState.isOpen = status;
        }

    }
});
