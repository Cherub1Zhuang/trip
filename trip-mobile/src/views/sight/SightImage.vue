<template>
    <!-- 景点图片 -->
    <div class="page-sight-image">
         <!-- 页面头部 -->
        <van-nav-bar left-text="返回" title="景点图片" left-arrow fixed @click-left="goBack" />
        <!-- //页面头部 -->
        <!-- 图片列表 -->
        <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
            <van-list
                class="sight-images"
                v-model:="loading"
                :error.sync='error'
                error-text="请求失败，点击重新加载"
                :finished="finished"
                finished-text="没有更多了"
                @load="getImagesList">
                <!-- 图片 -->
                <div class="img-imgs" @click="show=true">
                    <van-image width="120" height="120" :src="image.img" v-for="(image, index) in images" :key="index"/>
                </div>
                <van-image-preview v-model ="show" :images="imageUrls" @change="onChange" closeable>
                    <template v-slot:index>第{{ index+1 }}页</template>
                </van-image-preview>
                <!-- //图片 -->
            </van-list>
        </van-pull-refresh>
        <!-- //图片列表 -->

    </div>
</template>
<script>
import { ajax } from '@/utils/ajax'
import { SightApi } from '@/utils/apis'

export default {
    data () {
        return {
            id:'',
            images: [],
            show:false,
            index:0,
            currentPage:1,
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
    computed:{
        imageUrls () {
            return this.images.map(i => i.img)
        }
    },
    methods: {
        //   下拉刷新执行
        onRefresh() {
            //   清空数据
            this.images=[]
            this.currentPage=1
            this.finished=false
            this.error=false
            // 重新加载数据
            this.getImagesList()
        },
        goBack() {
            this.$router.go(-1)
        },
        getImagesList() {
            const url =SightApi.sightImageslUrl.replace('#{id}', this.id)
            ajax.get(url, {
                params: {
                    page:this.currentPage,
                    limit:21
                }
            }).then(({data: {meta, objects}}) => {
                this.images=this.images.concat(objects)
                // 加载状态接受
                this.loading=false
                // 设置下一页页码
                // this.currentPage=1
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
        // this.getImagesList()
    }
}
</script>
<style lang="less">
.page-sight-image{
    .sight-images{
        margin-top: 50px;
        .img-imgs{
            display: flex;
            flex-wrap: wrap;
            .van-image{
               margin: 5px 5px;
            }
        }
    }
}
</style>
