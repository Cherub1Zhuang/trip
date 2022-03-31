<template>
  <!-- 景点评论 -->
  <div class="page-sight-comment">
    <!-- 页面头部 -->
    <van-nav-bar left-text="返回" title="景点评论" left-arrow fixed @click-left="goBack" />
    <!-- //页面头部 -->
    <!-- 用户评价 -->
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
        <van-list
            class="sight-comment"
            v-model:="loading"
            :error.sync='error'
            error-text="请求失败，点击重新加载"
            :finished="finished"
            finished-text="没有更多了"
            @load="getCommentList">
        <comment-item v-for="item in commentList" :key="item.id" :itemp="item" />
        </van-list>
    </van-pull-refresh>
    <!-- //用户评价 -->
  </div>
</template>
<script>
// 评论相的组件
import CommentItem from '@/components/sight/CommentItem.vue'
import { ajax } from '@/utils/ajax'
import { SightApi } from '@/utils/apis'

export default {
    components:{
        CommentItem
    },
    data () {
        return {
            id:'',
            // 当前页码
            currentPage:1,
            // 评论列表
        commentList: [],
        // 正在加载中
        loading:false,
        // 所有的内容加载完
        finished:false,
        // 请求失败
        error:false,
        // 是否正在下拉刷新
        refreshing:false
        }
    },
  methods: {
    //   下拉刷新执行
      onRefresh() {
        //   清空数据
        this.commentList=[]
        this.currentPage=1
        this.finished=false
        this.error=false
        // 重新加载数据
        this.getCommentList()
      },
    goBack() {
      this.$router.go(-1)
    },
    // 评论列表接口
    getCommentList () {
      const url =SightApi.sightCommentlUrl.replace('#{id}', this.id)
      ajax.get(url, {
          params: {
              page:this.currentPage
          }
      }).then(({data: {meta, objects}}) => {
        this.commentList=this.commentList.concat(objects)
        // 加载状态接受
        this.loading=false
        // 设置下一页页码
        this.currentPage= meta.current_page+1
        // 数据全部加载完成：当前的页码==总页数
        if (meta.current_page===meta.page_count) {
            this.finished=true
        }
        this.refreshing=false
      }).catch(() => {
         this.loading = false
         this.error=true
         this.refreshing=false
      })
    },
    onChange(index) {
            this.index = index
        }
  },
  created() {
      this.id = this.$route.params.id
    //   this.getCommentList()
  }
}
</script>
<style lang="less">
.page-sight-comment{
    .sight-comment{
        margin-top: 50px;
        background-color: #fff;
    }
}
</style>
