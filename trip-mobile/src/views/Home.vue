<template>
  <div class="page-home">
    <!-- banner图 -->
    <Banner/>
    <!-- 热门景点推荐 -->
    <Hot/>
    <!-- //热门景点推荐 -->
    <!-- 精选景点 -->
    <Fine/>
    <!-- //精选景点 -->
    <!-- 底部导航 -->
    <trip-footer/>
    <!-- //底部导航 -->
  </div>
</template>

<script>
// @ is an alias to /src
// import { ajax } from '@/utils/ajax'
import Banner from '@/components/home/Banner.vue'
import Hot from '@/components/home/Hot.vue'
import Fine from '@/components/home/Fine'
import TripFooter from '@/components/common/Footer.vue'

export default {
  name: 'Home',
  components: {
    // banner图
    Banner,
    // 热门推荐
    Hot,
    // 精选景点
    Fine,
    // 底部导航
    TripFooter
  },
  created () {
  }
}
</script>
// <style lang="less" scoped>
// .page-home {}
// </style>
