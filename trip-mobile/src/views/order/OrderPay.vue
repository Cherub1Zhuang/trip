<template>
    <!-- 订单确认及支付 -->
    <div class="page-order-pay">
        <!-- banner -->
        <van-nav-bar
            title="订单支付"
            left-text="返回"
            right-text="取消订单"
            left-arrow
            @click-left="goBack"
            @click-right="onCancelOrder"
        />
        <!-- 订单号 -->
        <van-cell title="订单号" :value="sn" :title-style="{'text-align': 'left'}" />
        <!-- 票信息 -->
        <div class="order-info" v-for="item in orderDetail.items" :key="item.pk">
            <div class="left">
                <h3>{{ item.flash_name }}</h3>
                <div>
                    <van-icon name="clock-o" /> {{ item.remark }}
                </div>
                <!-- <div class="tips">短信接收</div> -->
            </div>
            <div class="right">
                <van-icon name="arrow" />
            </div>
        </div>
        <!-- 支付按钮 -->
        <van-submit-bar :price="orderDetail.buy_amount * 100" button-text="立即支付" @submit="onSubmit" />
    </div>
</template>
<script>
import { OrderApis } from '@/utils/apis'
import { ajax } from '@/utils/ajax'
import * as constants from '@/utils/constants'
export default {
    data () {
        return {
            // 订单流水号
            sn:'',
            // 订单信息
            orderDetail:{}
        }
    },
    methods: {
        // 获取订单的详细信息
        getOrderDetail () {
            const url = OrderApis.orderDetailUrl.replace('#{sn}', this.sn)
            ajax.get(url).then(({ data }) => {
                this.orderDetail = data
            })
        },
        // 确认支付
        onSubmit () {
            this.$dialog.confirm({
                    title: '确认支付',
                    message: `支付金额${this.orderDetail.buy_amount}`
                }).then(() => {
                    // 调用接口
                    const url = OrderApis.orderDetailUrl.replace('#{sn}', this.sn)
                    ajax.post(url).then(() => {
                        // 提示语
                        this.$notify({
                            type: 'success',
                            message: '支付成功'
                        })
                    })
                    // 跳转到订单列表
                    this.$router.replace({name: 'orderlist', params: {status: constants.ORDER_STATUS_ALL}})
                })
        },
        goBack() {
            this.$dialog.confirm({
                    title: '温馨提示',
                    message: '您还没有支付，确认放弃支付吗？'
                }).then(() => {
                    // on confirm
                    this.$router.go(-1)
                })
        },
        onCancelOrder () {
            this.$dialog.confirm({
                    title: '温馨提示',
                    message: '确认取消该订单吗？'
                }).then(() => {
                    // TODO 调用接口
                    const url = OrderApis.orderDetailUrl.replace('#{sn}', this.sn)
                    // put方式调用接口
                    ajax.put(url).then(res => {
                        console.log(res)
                        // 给用户提示
                        if (res.status === 201) {
                            this.$notify({
                                type: 'success',
                                message: '订单已取消成功'
                            })
                        } else if (res.status === 200) {
                            this.$notify({
                                type: 'warning',
                                message: '订单已取消,请勿重复操作'
                            })
                        }
                        this.$router.go(-1)
                    })
                })
        }
    },
    created () {
        // 获取订单流水号
        this.sn = this.$route.params.sn
        // 获取订单信息
        this.getOrderDetail()
    }
}
</script>
<style lang="less">
.page-order-pay{
    .order-info{
        display: flex;
        padding: 10px;
        background-color: #fff;
        margin-top: 10px;
        .left{
            flex: 1;
            text-align: left;
            h3 {
                padding: 5px 0;
                margin: 0;
            }
        }
        .right{
            width: 80px;
        }
    }
}
</style>
