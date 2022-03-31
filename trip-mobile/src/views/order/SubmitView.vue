<template>
    <!-- 填写订单 -->
    <div class="page-order-submit">
        <!-- banner -->
        <van-nav-bar left-text="返回" title="填写订单" left-arrow @click-left="goBack" />
        <!-- 门票信息 -->
        <div class="order-info">
            <div class="left">
                <h3>{{ ticketDetail.name }}</h3>
                <div class="tips">{{ ticketDetail.desc }}</div>
                <div class="tags">
                    <span>
                        <van-icon name="clock-o" />明日可定
                    </span>
                    <span>
                        <van-icon name="clock-o" />条件退
                    </span>
                </div>
            </div>
            <div class="right">
                <div class="text-waring">￥{{ ticketDetail.sell_price }}/张</div>
                <van-button plain hairline type="info" size="mini" @click="showPopup=true">预定须知</van-button>
                <van-popup
                    v-model="showPopup"
                    closeable
                    position="bottom"
                    :style="{ height: '80%' }"
                >
                    <TicketTips :ticketDetail="ticketDetail"/>
                </van-popup>
            </div>
        </div>
        <!-- 订单信息表单 -->
        <van-form @submit="onSubmit" class="form-box">
            <van-cell-group class="form-group">
                <van-cell title="出行日期" :value="form.play_date" @click="showCalendar = true" />
                <van-calendar v-model="showCalendar" @confirm="onConfirm" />
            </van-cell-group>
            <van-cell-group class="form-group">
                <van-cell title="购买数量">
                    <van-stepper v-model="form.buy_count" integer min="1"/>
                </van-cell>
            </van-cell-group>
            <van-cell-group class="form-group">
                <van-field
                    required
                    v-model="form.to_user"
                    label="收件人"
                    placeholder="请输入收件人"
                    :rules="[{ required: true, message: '请填写收件人' }]"
                />
                <van-field
                    required
                    v-model="form.to_phone"
                    label="手机号"
                    placeholder="请输入手机号"
                    :rules="[{ required: true, message: '请填写手机号' }]"
                />
            </van-cell-group>
            <div>
                <van-submit-bar :price="totalPrice" button-text="提交订单"/>
            </div>
        </van-form>
    </div>
</template>
<script>
import { ajax } from '@/utils/ajax'
import { OrderApis, SightApi } from '@/utils/apis'
import { mapState } from 'vuex'
import TicketTips from '@/components/sight/TicketTips.vue'
// import * as types from '@/store/mutation-types'
export default {
    components: {
        TicketTips
    },
    data () {
        return {
            // 门票id
            id: '',
            // 门票详情
            ticketDetail: {},
            // 预定须知弹窗开关
            showPopup:false,
            // 日期弹窗开关
            showCalendar:false,
            // 表单数据
            form: {
                // 出行日期
                play_date:'',
                // 购买数量
                buy_count:1,
                // 收件人
                to_user:'',
                // 收件人手机号
                to_phone:''
            }
        }
    },
    computed: {
        totalPrice () {
            return this.ticketDetail.sell_price * this.form.buy_count * 100
        },
        // 从vuex中读取数据
        ...mapState({
            phoneNum: state => state.user.username,
            nickName: state => state.user.nickname
        })
    },
    methods: {
        getTicketDetail () {
            ajax.get(SightApi.ticketDetaillUrl.replace('#{id}', this.id)).then(({ data }) => {
                this.ticketDetail = data
                console.log(data)
            })
        },
        goBack () {
            this.$router.go(-1)
        },
        formatDate (date) {
            return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
        },
        onConfirm (date) {
            this.showCalendar=false
            this.form.play_date=this.formatDate(date)
        },
        onSubmit () {
            console.log('提交表单')
            // ajax接口调用
            ajax.post(OrderApis.ticketSubmitUrl, {
                ticket_id: this.id,
                ...this.form
            }).then(({ data }) => {
                // 提示用户
                this.$notify({
                    type: 'success',
                    message: '提交成功，请支付'
                })
                // 跳转到待支付页面
                this.$router.replace({name: 'orderpay', params: {sn: data.sn}})
            })
        }
    },
    created () {
        // 门票id
        this.id = this.$route.params.id
        // 获取门票信息
        this.getTicketDetail()
        this.form.to_user = this.nickName || ''
        this.form.to_phone = this.phoneNum || ''
        console.log('created', this.nickName, this.form.to_user, this.$store.state.user.username)
    }
}
</script>
<style lang="less">
.page-order-submit{
    .order-info{
        display: flex;
        padding: 10px;
        background-color: #fff;
        .left{
            flex: 1;
            text-align: left;
            h3{
                margin: 0;
                padding: 5px 0;
            }
            tips{
                padding: 10px 0;
                color: #999;
                font-size: 12px;
            }
            .tags{
                font-size: 12px;
            }
        }
        .right{
            width: 90px;
            text-align: right;
        }
    }
    .form-box{
        margin-top: 10px;
        .form-group{
            margin-bottom: 10px;
            .van-cell{
                text-align: left;
            }
        }
    }
}
</style>
