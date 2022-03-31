<template>
    <!-- 短信验证码逻辑 -->
    <van-button size="small" type="primary" @click.prevent="sendSmsCode()" :disabled="isSmsSend">{{ sendBtnText }}</van-button>
</template>
<script>
import {SystemApis} from '@/utils/apis'
import { ajax } from '@/utils/ajax'
export default {
    props:['phoneNum'],
    data () {
        return {
            // 是否已经发送验证码
            isSmsSend: false,
            sendBtnText:'点击发送验证码',
            counter: 5,
            timer: null
        }
    },
    methods: {
        reset () {
            this.isSmsSend = false
            this.sendBtnText = '点击发送验证码'
            if (this.timer) {
                clearInterval(this.timer)
                this.counter = 5
                this.timer = null
            }
        },
        countDown () {
            // 倒计时
            this.timer = setInterval(() => {
                this.sendBtnText=`(${this.counter}秒)后重新发送`
                this.counter--
                if (this.counter<0) {
                    this.reset()
                }
            }, 1000)
        },
        sendSmsCode () {
            // 判断手机号是否已经输入
            if (!this.phoneNum) {
                this.$notify('请输入手机号')
                return false
            }
            // 调用接口，发送短信验证码
            ajax.post(SystemApis.sendSmsCodeUrl, {
                phone_num:this.phoneNum
            }).then(({ data }) => {
                this.$notify({
                    message: `验证码为：${data.sms_code}，${data.timeout / 60}分钟内有效`,
                    duration: 1000*10,
                    type: 'success'
                })
                this.isSmsSend = true
                // 开机倒计时60是，之后才能再次点击
                this.countDown()
            }).catch(err => {
                this.reset()
                console.log(err)
            })
        }
    }
}
</script>
