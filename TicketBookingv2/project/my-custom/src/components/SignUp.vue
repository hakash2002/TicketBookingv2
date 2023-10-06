<template>
    <div class="img2a signup">
        <form @submit.prevent="signupaction" method="post">
            <div class="form2a">
                <div class="title2a">Welcome</div>
                <div class="subtitle2a">Let's create your account!</div>
                <div class="input-container2a ic12a">
                    <input id="userid" class="input2a" type="text" placeholder=" " name="userid" v-model="userid" required />
                    <div class="cut2"></div>
                    <label for="userid" class="placeholder2a">UserID</label>
                </div>
                <div class="input-container2a ic22a">
                    <input id="username" class="input2a" type="text" placeholder=" " name="username" v-model="username"
                        required />
                    <div class="cut2a"></div>
                    <label for="username" class="placeholder2a">Username</label>
                </div>
                <div class="input-container2a ic22a">
                    <input id="password" class="input2a" type="password" placeholder=" " name="password" v-model="password"
                        required />
                    <div class="cut2a"></div>
                    <label for="password" class="placeholder2a">Password</label>
                </div>
                <div class="input-container2a ic22a">
                    <input id="email" class="input2a" type="email" placeholder=" " name="email" v-model="email"
                        required />
                    <div class="cut2a"></div>
                    <label for="password" class="placeholder2a">Email-ID</label>
                </div>
                <button type="submit" class="submit2a">Sign Up</button>
            </div>
            <br><br>
        </form>
    </div>
</template>

<script>
import axios from 'axios'
import router from '../router'

export default {
    data() {
        return {
            userid: '',
            password: '',
            username: '',
            email: '',
        }
    },
    methods: {
        async signupaction() {
            try {
                // Dispatch Vuex action to handle login
                const response = await axios.post('http://127.0.0.1:5000/signup', {
                    userid: this.userid,
                    password: this.password,
                    username: this.username,
                    email: this.email
                });
                localStorage.setItem('token',response.data.access_token)
                router.push('/shows')
            }
            catch (error) {
                // Handle errors from POST and GET requests
                if (error.response.status === 402) {
                    alert("Userid already exists try another name")
                } else {
                    console.error('Error in POST or GET request:', error);
                }
            }
        },
    }
}

</script>
<style scoped>
@import '../assets/styles/signup.css';

</style>