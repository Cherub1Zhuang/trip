<template>
<!-- 用户登录 -->
    <div class="page-account-login">
        <!-- 导航条 -->
        <van-nav-bar left-text="返回" title="用户登录" left-arrow fixed @click-left="goBack" />
        <!-- 表单输入 -->
        <div class="login-form">
            <van-form @submit="onSubmit">
                <van-cell-group inset>
                    <van-field
                    v-model="username"
                    name="用户名"
                    label="用户名"
                    placeholder="用户名"
                    type="tel"
                    maxlength="11"
                    clearable
                    :rules="ruleName"
                    />
                    <van-field
                    v-model="password"
                    type="password"
                    name="密码"
                    label="密码"
                    placeholder="密码"
                    clearable
                    :rules="[{ required: true, message: '请填写密码' }]"
                    />
                </van-cell-group>
                <div style="margin: 16px;">
                    <van-button round block type="primary" native-type="submit">
                    提交
                    </van-button>
                </div>
            </van-form>
        </div>

        <!-- 文字提示 -->
        <div class="tips">
            登录表示同意 <a href="#">用户使用协议</a>及 <a href="#">隐私条款</a>
        </div>
        <div class="tips">
            没有账号？ <router-link :to="{name: 'accountregister'}">点击注册>></router-link>
        </div>
        <!-- 版权信息 -->
        <Copyright/>
    </div>
</template>
<script>
import Copyright from '@/components/common/Copyright.vue'
import {AccountsApis} from '@/utils/apis'
import { ajax } from '@/utils/ajax'
import * as types from '@/store/mutation-types'
export default {
    components:{
        Copyright
    },
    data () {
        return {
            ruleName:[
                { required: true, message: '请填写用户名' },
                { pattern: /1\d{10}/, message: '请填正确的手机号' }
                ],
            username: '',
            password: ''
        }
    },
    methods: {
        goBack() {
            this.$router.go(-1)
        },
        onSubmit () {
            // 提交表单
            // 1调用接口
            ajax.post(AccountsApis.loginUrl, {
                username: this.username,
                password: this.password
            }).then(({data}) => {
                // 2拿到用户信息存储到vuex
                this.$store.commit(types.UPDATE_USER_INFO, data)
                this.$toast('登录成功')
                this.$router.replace({name:'mine'})
            }).catch(({response: {data}}) => {
                console.log(data)
                this.$toast(`${data.error_code},${data.error_msg}`)
            })
            // 3如果出现异常需要给用户提示
        }
    }
}
</script>
<style lang="less">
.page-account-login{
    .login-form{
        margin-top: 60px;
    }
}
</style>
