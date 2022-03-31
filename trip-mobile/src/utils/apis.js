/**
 * 存放项目中所有接口地址
 */
// const apiHost='http://localhost:8080/api'
const apiHost='/api'
/**
 * 用户账户相关的接口
 */
const AccountsApis = {
    // 用户登录
    loginUrl:apiHost+'/accounts/user/api/login/',
    // 用户退出登录
    logoutUrl:apiHost+'/accounts/user/api/logout/',
    // 用户信心
    userInfoUrl:apiHost+'/accounts/user/api/info/',
    // 用户注册
    registerUrl:apiHost+'/accounts/user/api/register/'
}

/**
 * 系统模块接口
 */
const SystemApis = {
    // 轮播图列表
    sliderListUrl:apiHost+'/system/slider/list/',
    // 发动短信验证码
    sendSmsCodeUrl:apiHost+'/system/send/sms/'
}

/**
 * 景点模块
 */
const SightApi = {
    // 景点列表
    sightListUrl:apiHost+'/sight/sight/list/',
    // 缓存优化的url
    sightListCacheUrl:apiHost+'/sight/sight/list/cache/',
    // 景点详情
    sightDetailUrl:apiHost+'/sight/sight/detail/#{id}/',
    // 门票列表
    sightTicketlUrl:apiHost+'/sight/ticket/list/#{id}/',
    // 评论列表
    sightCommentlUrl:apiHost+'/sight/comment/list/#{id}/',
    // 景点图片列表
    sightImageslUrl:apiHost+'/sight/sight/images/#{id}/',
    // 门票详情
    ticketDetaillUrl:apiHost+'/sight/ticket/detail/#{id}/'
}

const OrderApis = {
    // 订单列表
    orderListUrl:apiHost+'/order/order/list/',
    // 订单详情、订单支付、订单删除、订单取消
    orderDetailUrl:apiHost+'/order/order/detail/#{sn}/',
    // 提交订单
    ticketSubmitUrl:apiHost+'/order/ticket/submit/'
}

export {
    AccountsApis,
    SystemApis,
    SightApi,
    OrderApis
}
