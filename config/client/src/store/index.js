import { createStore } from 'vuex';

export default createStore({
    state: {
        modalState: {
            isOpen: false,
        },
        signupFormState: {
            isOpen: false,
        },
        userState: {
            isLoggedIn: false,
            authToken: '',
            userName: '',
            emailAddress: ''
        }
    },
    getters: {
        getModalState(state) {
            console.log("getModalState from store");
            return state.modalState.isOpen;
        },
        getSignupFormState(state) {
            return state.signupFormState.isOpen;
        },
        getLoggedInState(state) {
            return state.userState.isLoggedIn;
        },
        getAuthToken(state) {
            return state.userState.authToken;
        },
        getUserName(state) {
            return state.userState.userName;
        }
    },
    mutations: {
        toggleModalState: function(state, status) {
            console.log("toggelModalState to store");
            state.modalState.isOpen = status;
        },
        toggleSignupFormState: function(state, status) {
            state.signupFormState.isOpen = status;
        },
        toggleLoginState: function(state, status) {
            state.userState.isLoggedIn = status;
        },
        updateAuthToken: function(state, token) {
            state.userState.authToken = token;
        },
        updateUserState: function(state, data) {
            state.userState.userName = data.name;
            state.userState.emailAddress = data.emailAddress;
        }
    }
});
