import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/Home.vue'
import SearchView from '../views/SearchView.vue'
import MineView from '../views/MineView.vue'
import SightList from '../views/sight/SightList.vue'
import SightInfo from '../views/sight/SightInfo.vue'
import SightComment from '../views/sight/SightComment.vue'
import SightImage from '../views/sight/SightImage.vue'
import SightDetail from '../views/sight/SightDetail.vue'
import AccountLogin from '../views/accounts/LoginView.vue'
import AccountRegister from '../views/accounts/RegisterView.vue'
import SubmitView from '../views/order/SubmitView.vue'
import OrderPay from '../views/order/OrderPay.vue'
import OrderList from '../views/order/OrderList.vue'
import OrderView from '../views/order/OrderView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/search',
    name: 'search',
    component: SearchView
  },
  // 景点列表
  {
    path: '/sight/list',
    name: 'sightlist',
    component: SightList
  },
  // 景点详情
  {
    path: '/sight/detail/:id',
    name: 'sightdetail',
    component: SightDetail
  },
  // 景点介绍
  {
    path: '/sight/info/:id',
    name: 'sightinfo',
    component: SightInfo
  },
  // 景点评论
  {
    path: '/sight/comment/:id',
    name: 'sightcomment',
    component: SightComment
  },
  // 景点图片
  {
    path: '/sight/image/:id',
    name: 'sightimage',
    component: SightImage
  },
  // 登录页面
  {
    path: '/account/login',
    name: 'accountlogin',
    component: AccountLogin
  },
  // 用户注册
  {
    path: '/account/register',
    name: 'accountregister',
    component: AccountRegister
  },
  // 个人中心
  {
    path: '/mine',
    name: 'mine',
    component: MineView
  },
  // 提交订单
  {
    path: '/order/submit/:id',
    name: 'ordersubmit',
    component: SubmitView
  },
  // 确认订单并支付
  {
    path: '/order/pay/:sn',
    name: 'orderpay',
    component: OrderPay
  },
  // 确认订单并支付我的订单列表
  {
    path: '/order/list/:status',
    name: 'orderlist',
    component: OrderList
  },
  // 查看订单
  {
    path: '/order/view/:sn',
    name: 'orderview',
    component: OrderView
  }
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // }
]

const router = new VueRouter({
  routes
})

export default router
