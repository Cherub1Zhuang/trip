<template>
<!-- 用户注册 -->
    <div class="page-account-register">
        <!-- 导航条 -->
        <van-nav-bar left-text="返回" title="用户登录" left-arrow fixed @click-left="goBack" />
        <!-- 表单输入 -->
        <div class="register-form">
            <van-form @submit="onSubmit">
                <van-cell-group inset>
                    <van-field
                    v-model="form.username"
                    label="手机号码"
                    placeholder="手机号码"
                    @input="onPhoneChange"
                    type="tel"
                    maxlength="11"
                    clearable
                    :rules="ruleName"
                    />
                    <van-field
                        v-model="form.sms_code"
                        center
                        clearable
                        label="短信验证码"
                        placeholder="请输入短信验证码"
                        :rules="[{ required: true, message: '请填写短信验证码' }]"
                    >
                        <template #button>
                            <SendSmsCode ref="refSms" :phoneNum="form.username"/>
                        </template>
                    </van-field>
                    <van-field
                        v-model="form.nickname"
                        label="用户昵称"
                        placeholder="用户昵称"
                        maxlength="32"
                        clearable
                        :rules="[{ required: true, message: '请填写用户昵称' }]"
                    />
                    <van-field
                    v-model="form.password"
                    type="password"
                    label="密码"
                    placeholder="密码"
                    clearable
                    :rules="[{ required: true, message: '请填写密码' }]"
                    />
                    <van-field
                    v-model="form.passwordRepeat"
                    type="password"
                    label="确认密码"
                    placeholder="确认密码"
                    clearable
                    :rules="rulePassword"
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
            注册表示同意 <a href="#">用户使用协议</a>及 <a href="#">隐私条款</a>
        </div>
        <div class="tips">
            已有账号 <router-link :to="{name: 'accountlogin'}">点击登录>></router-link>
        </div>
        <!-- 版权信息 -->
        <Copyright/>
    </div>
</template>
<script>
import Copyright from '@/components/common/Copyright.vue'
import SendSmsCode from '@/components/common/SendSmsCode.vue'
import {AccountsApis} from '@/utils/apis'
import { ajax } from '@/utils/ajax'
import * as types from '@/store/mutation-types'
export default {
    components:{
        Copyright,
        SendSmsCode
    },
    data () {
        return {
            ruleName:[
                { required: true, message: '请填写用户名' },
                { pattern: /1\d{10}/, message: '请填正确的手机号' }
                ],
            // 重复密码验证
            rulePassword:[
                    { required: true, message: '请填写确认密码' },
                    { validator : () => this.form.password===this.form.passwordRepeat, message: '两次密码输入不一致' }
                ],
            username: '',
            password: '',
            form: {
                username:'',
                nickname:'',
                sms_code:'',
                password:'',
                passwordRepeat:''
            }
        }
    },
    methods: {
        // 手机号发生变化时，重置验证码状态
        onPhoneChange () {
            this.$refs.refSms.reset()
        },
         goBack() {
            this.$router.go(-1)
        },
        onSubmit () {
            // 提交表单
            // 1调用接口
            ajax.post(AccountsApis.registerUrl, {
                username: this.form.username,
                password: this.form.password,
                sms_code: this.form.sms_code,
                nickname: this.form.nickname
            }).then(({data}) => {
                // 2成功返回，用户信息写入vuex
                this.$store.commit(types.UPDATE_USER_INFO, data)
                // 3提示用户
                this.$notify({
                    message: '注册成功',
                    type: 'success'
                })
                // 4跳转到个人中心
                this.$router.push({name: 'mine'})
            })
        }
    }
}
</script>
<style lang="less">
.page-account-register{
    .register-form{
        margin-top: 60px;
    }
}
</style>
