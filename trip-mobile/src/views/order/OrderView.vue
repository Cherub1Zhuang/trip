<template>
    <div class="page-order-view">
        <!-- 导航条 -->
        <van-nav-bar
        title="订单详情"
        left-text="返回"
        :right-text="constants.ORDER_STATUS[orderDetail.status]"
        left-arrow
        @click-left="goBack"
        />
        <!-- 订单信息 -->
        <p>订单信息</p>
        <div class="order-info">
            <van-cell title="订单号" :value="orderDetail.sn" />
            <van-cell title="下单时间" :value="orderDetail.created_at" />
        </div>
        <!-- 订单明细 -->
        <p>订单明细</p>
        <div class="order-content">
            <div class="order-items">
                <div class="item" v-for="(item,index) in orderDetail.items" :key="index">
                    <p>商品{{index+1}}</p>
                    <div class="item-body">
                        <div class="left">
                            <van-image width="100" height="100" :src="item.flash_img" />
                        </div>
                        <div class="right">
                            <div class="title">{{ item.flash_name }}</div>
                            <div class="num-price">数量：{{ item.count }} 价格： ￥{{ item.amount }}</div>
                            <div class="time">{{ item.remark }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- 订单总计 -->
        <p>订单总计</p>
        <div class="footer">
            <div class="total">总公{{orderDetail.buy_count}}件商品，合计￥{{orderDetail.buy_amount}}</div>
            <van-button round type="warning" size="small" v-if="orderDetail.status === constants.ORDER_STATUS_PAY" @click="goPay">去支付</van-button>
            <van-button round type="warning" size="small" @click="goDelete" v-else>删除订单</van-button>
        </div>
    </div>
</template>
<script>
import { ajax } from '@/utils/ajax'
import { OrderApis } from '@/utils/apis'
import * as constants from '@/utils/constants'
export default {
    data () {
        return {
            constants,
            sn: '',
            orderDetail: {}
        }
    },
    methods: {
        goBack () {
            // this.$router.push({name: 'orderlist', params: {status: this.orderDetail.status}})
            this.$router.go(-1)
        },
        goPay () {
            this.$router.push({name:'orderpay', params: {sn: this.orderDetail.sn}})
        },
        goDelete () {
            // 弹框确认
            this.$dialog.alert({
                title: '温馨提示',
                message: '删除订单将无法恢复，确认删除订单？'
            }).then(() => {
                // 调用接口
                const url = OrderApis.orderDetailUrl.replace('#{sn}', this.orderDetail.sn)
                ajax.delete(url).then(res => {
                    if (res.status === 201) {
                        // 告诉用户
                        this.$notify({
                            type: 'success',
                            message: '删除成功'
                        })
                        // 隐藏界面显示
                        this.goBack()
                    }
                })
            })
        },
        getOrderDetail() {
            const url = OrderApis.orderDetailUrl.replace('#{sn}', this.sn)
            ajax.get(url).then(({data}) => {
                this.orderDetail=data
            })
        }
    },
    created () {
        this.sn = this.$route.params.sn
        console.log(this.sn)
        this.getOrderDetail()
    }
}
</script>
<style lang="less">
.page-order-view{
    p{
        text-align: left;
        padding-left: 10px;
    }
    .order-info{
        .van-cell__title{
            text-align: left;
        }
    }
    .order-content{
        .order-items{
            background-color: #fff;
            .item{
                border-bottom: 1px solid #f0efef;
                p{
                    padding-top: 10px;
                }
                .item-body{
                    display: flex;
                    padding-bottom: 10px;
                    .left{
                        margin-left: 10px;
                        }
                    .right{
                        margin-left: 10px;
                        text-align: left;
                        .title{
                            font-size: 21px;
                        }
                        .num-price{
                            font-size: 15px;
                            color: #636060;
                        }
                        .time{
                            font-size: 14px;
                            color: rgb(170, 163, 163);
                        }
                    }
                }
            }
        }
    }
    .footer{
        background-color: #fff;
        text-align: right;
        .total{
            padding-top: 10px;
            margin-right: 10px;
        }
        .van-button{
            margin: 10px auto;
            margin-right: 15px;
        }
    }
}
</style>
