<template>
  <!-- 底部导航（公共组件） -->
  <div>
    <van-tabbar v-model="active" route>
      <van-tabbar-item name="home" icon="wap-home-o" :to="{name:'home'}">首页</van-tabbar-item>
      <van-tabbar-item name="search" icon="search" :to="{name:'search'}">搜索</van-tabbar-item>
      <van-tabbar-item name="mine" icon="user-o" :to="{name:'mine'}">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>
<script>
export default {
    data () {
        return {
            active: 'home'
        }
    }
}
</script>
