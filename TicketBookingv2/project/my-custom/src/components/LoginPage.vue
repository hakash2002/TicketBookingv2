<template>
    <div class="body1">
        <form @submit.prevent="login" method="post">
            <div class="form img">
                <div class="title">Sign In</div>
                <div class="input-container ic1">
                    <input id="userid" class="input" type="text" placeholder=" " name="userid" v-model="user_id" required>
                    <div class="cut"></div>
                    <label for="userid" class="placeholder">UserID</label>
                </div>
                <div class="input-container ic2">
                    <input id="password" class="input" type="password" placeholder=" " name="password" v-model="password"
                        required>
                    <div class="cut"></div>
                    <label for="password" class="placeholder">Password </label>
                </div>
                <button type="submit" class="submit">Login</button>
                <br><br><br>
                <a href="/register" class="title" style="font-size: 15px;">New User?</a>
            </div>
        </form>
    </div>
</template>

<script>
import store from '../store';
export default {
    data() {
        return {
            user_id: '',
            password: '',
        };
    },
    methods: {
        async login() {
            try {
                // Dispatch Vuex action to handle login
                await store.dispatch('login', {
                    user_id: this.user_id,
                    password: this.password,
                });
                const lastVisitedUrl = localStorage.getItem('lastVisitedUrl');
                if (lastVisitedUrl) {
                    localStorage.removeItem('lastVisitedUrl');

                    this.$router.replace(lastVisitedUrl);
                } else {
                    this.$router.replace('/shows');
                }

            }
            catch (error) {
                // Handle errors from POST and GET requests
                if (error.response.status === 401) {
                    alert("Sorry,Invalid credentials")
                } 
                if (error.response.status === 405) {
                    alert("Sorry,check userid for any spelling mistakes")
                }
            }
        },
        saveLastVisitedUrl() {
            const currentUrl = this.$route.fullPath;
            localStorage.setItem('lastVisitedUrl', currentUrl);
        },
        goToLoginPage() {
            if (this.$route.path !== '/login') {
                this.$router.push('/login');
            }
        }
    },
created(){
    window.addEventListener('beforeunload', this.saveLastVisitedUrl);



},
beforeDestroy() {
    window.removeEventListener('beforeunload', this.saveLastVisitedUrl);

}

};
</script>

<style scoped>
@import '../assets/styles/loginpage.css';
</style>
