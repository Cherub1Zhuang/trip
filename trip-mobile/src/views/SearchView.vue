<template>
  <!-- 搜索页面 -->
  <div class="page-search">
    <!-- 标题 -->
    <van-nav-bar left-text="返回" left-arrow @click-left="goBack" title="景点列表" v-if="isFromHome"/>
    <van-nav-bar title="搜索景点" v-else/>
    <!-- //标题 -->
    <!-- 搜索框 -->
    <van-search
      v-model="sightName"
      show-action
      label="景点"
      placeholder="请输入搜索关键词"
      @search="onSearch"
      @clear= 'clear'
    >
      <template #action>
        <div @click="onSearch">搜索</div>
      </template>
    </van-search>

    <!-- //搜索框 -->
    <h2 v-if="isHot">热门推荐</h2>
    <h2 v-if="isTop">精选景点</h2>
    <!-- 景点列表 -->
    <div class="sight-list">
        <sight-item v-for="item in dataList" :key="item.id" :itemp="item"/>
    </div>
    <!-- //景点列表 -->
    <!-- 分页 -->
    <van-pagination v-model="currentPage" :total-items="totalItems" :items-per-page="perPage" @change="pageChange"/>
    <!-- //分页 -->
    <!-- 页脚 -->
    <trip-footer v-if="!isFromHome"/>
    <!-- //页脚 -->
  </div>
</template>
<script>
// 景点列表的每一项
import SightItem from '@/components/common/ListSight.vue'
// 页脚
import TripFooter from '@/components/common/Footer.vue'
// 接口引用
import { ajax } from '@/utils/ajax'
import { SightApi } from '@/utils/apis'
export default {
    components: {
        SightItem,
        TripFooter
    },
    data () {
        return {
            // 搜索景点名称
            sightName:'',
            // 景点列表的数据
            dataList:[],
            // 记录总数
            totalItems: 0,
            // 当前页码
            currentPage: 1,
            // 每一页的数据大小
            perPage: 5,
            // 判读是否是热门和精选景点
            isHot: '',
            isTop: ''
        }
    },
    computed: {
      isFromHome () {
        return this.isHot || this.isTop
      }
    },
    methods: {
        goBack() {
        this.$router.go(-1)
        },
        clear() {
          // 重置数据
          this.dataList=[]
          this.curremtPage=1
          // 执行查询
          this.getDataList()
        },
        // 页码发生变化调用
        pageChange() {
          this.getDataList()
        },
        onSearch() {
            // 判断搜索内容是否为空
            if (!this.sightName) {
              this.$toast('请输入搜索词')
              return
            }
            // 重置数据
            this.dataList=[]
            this.currentPage=1
            // 执行查询
            this.getDataList()
        },
        // 景点列表的接口
        getDataList() {
            ajax.get(SightApi.sightListUrl, {
                params: {
                    page: this.currentPage,
                    name: this.sightName,
                    limit: this.perPage,
                    is_top:this.isTop,
                    is_hot:this.isHot
                }
            }).then(({ data: {meta, objects } }) => {
                this.dataList=objects
                // 总记录数
                this.totalItems = meta.total_count
            })
        }
    },
    mounted () {
      this.isHot=this.$route.query.isHot
      this.isTop=this.$route.query.isTop
      this.getDataList()
    }
    // watch: {
    //   sightName (to, from) {
    //     if (this.sightName==='') {
    //       this.onSearch()
    //     }
    //   }
    // }
}
</script>
<style lang="less">
.page-search{
  padding-bottom: 60px;
  h2{
    font-size: 16px;
    text-align: left;
    padding: 5px 10px;
    margin: 0;
    margin-bottom: -10px;
  }
  .sight-list{
    padding: 10px;
    background-color: #fff;
    margin: 10px 0;
  }
}
</style>
