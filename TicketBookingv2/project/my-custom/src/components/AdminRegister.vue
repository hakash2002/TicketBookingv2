<template>
    <div class="img2a signup">
        <form @submit.prevent="register">
            <div class="form2a">
                <div class="title2a">Welcome</div>
                <div class="subtitle2a">Let's create new account!</div>
                <div class="input-container2a ic12a">
                    <input id="adminid" class="input2a" type="text" placeholder=" " name="adminid" v-model="id" required />
                    <div class="cut2a"></div>
                    <label for="userid" class="placeholder2a">AdminID</label>
                </div>
                <div class="input-container2a ic22a">
                    <input id="password" class="input2a" type="password" placeholder=" " name="password" v-model="pword"
                        required />
                    <div class="cut2a"></div>
                    <label for="password" class="placeholder2a">Password</label>
                </div>
                <button type="submit" class="submit2a">Sign Up</button>
            </div>
            <br><br>
        </form>
    </div>
</template>
<script>
import axios from 'axios';
import router from '../router'

export default {
    data() {
        return {
            id : '',
            pword : '',
        }
    },
    methods: {
        async register() {
            try {
                console.log(this.id)
                const response = await axios.post('http://127.0.0.1:5000/admin/register', {
                    adminid: this.id,
                    password: this.pword,
                });
                console.log(response.data.message)
                alert(response.data.message)
                localStorage.setItem('admintoken', response.data.access_token)
                localStorage.setItem('username', response.data.username)
                router.push('/admindash');
            }
            catch (error) {
                // Handle errors from POST and GET requests
                alert(error.response.message)
            }
        },
    }
}
</script>