<template>
  <!-- 竞选景点 -->
  <div class="home-fine-box">
    <!-- 顶上导航 -->
    <van-cell
      icon="location-o"
      title="精选景点"
      title-style="text-align:left"
      value="更多"
      is-link
      :to="{name:'search', query:{isTop:1}}"
    />
    <!-- //顶上导航 -->
    <!-- 景点列表 -->
    <div class="box-main">
        <SightItem v-for="item in dataList" :key="item.id" :itemp="item"/>
    </div>
    <!-- //景点列表 -->
  </div>
</template>
<script>
import SightItem from '@/components/common/ListSight.vue'
import { ajax } from '@/utils/ajax'
import { SightApi } from '@/utils/apis'
export default {
    components: {
        SightItem
    },
    data () {
        return {
            dataList:[]
        }
    },
    methods: {
        // 查询精选景点的数据
        getDataList() {
            ajax.get(SightApi.sightListCacheUrl, {
                params: {
                    is_top: 1
                }
            }).then(({ data }) => {
                this.dataList=data.objects
            })
        }
    },
    created () {
        this.getDataList()
    }
}
</script>
<style lang="less">
.home-fine-box {
    padding: 0 10px;
    .van-cell{
        padding: 10px 0;
    }
  .box-main {
    padding-bottom: 50px;
  }
}
</style>
