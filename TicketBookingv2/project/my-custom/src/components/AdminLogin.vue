<template>
    <div class="img3 adminlogin">
        <form @submit.prevent="login" method="post">
            <div class="form9">
                <div class="title4a">Sign In</div>
                <div class="input-container3 ic13">
                    <input id="userid" class="input3" type="text" placeholder=" " name="userid" v-model="adminid" required>
                    <div class="cut3"></div>
                    <label for="userid" class="placeholder3">AdminID</label>
                </div>
                <div class="input-container3 ic23">
                    <input id="password" class="input3" type="password" placeholder=" " name="password" v-model="password"
                        required>
                    <div class="cut3"></div>
                    <label for="password" class="placeholder3">Password </label>
                </div>
                <button type="submit" class="submit3">Login</button>
                <br><br>
                <a href="/admin/register" class="aus" style="font-size: 15px;">New Register?</a>
            </div>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            adminid: '',
            password: '',
        }
    },
    methods: {
        async login() {
            try {
                // Dispatch Vuex action to handle login
                const response = await axios.post('http://127.0.0.1:5000/admin/login', {
                    adminid: this.adminid,
                    password: this.password,
                });
                localStorage.setItem('admintoken', response.data.access_token)
                localStorage.setItem('username', response.data.username)
                const lastVisitedUrl = localStorage.getItem('lastVisitedUrladm');
                if (lastVisitedUrl && lastVisitedUrl != '/admin/login') {
                    localStorage.removeItem('lastVisitedUrladm');

                    this.$router.replace(lastVisitedUrl);
                } else {
                    this.$router.replace('/admindash');
                }

            }
            catch (error) {
                // Handle errors from POST and GET requests
                if (error.response.status === 401) {
                    alert("Sorry, Invalid credentials")
                }
                if (error.response.status === 405) {
                    alert("Sorry, check adminid for any spelling mistakes")
                }
            }
        },
        saveLastVisitedUrladm() {
            const currentUrl = this.$route.fullPath;
            localStorage.setItem('lastVisitedUrladm', currentUrl);
        },
    },
    created() {
        window.addEventListener('beforeunload', this.saveLastVisitedUrladm);
    },
    beforeDestroy() {
        window.removeEventListener('beforeunload', this.saveLastVisitedUrladm);

    }

}
</script>
<style scoped>
@import '../assets/styles/adminlogin.css';
</style>