const { defineConfig } = require('@vue/cli-service')
// Node.js里面的模块
module.exports = defineConfig({
  transpileDependencies: true,
  // http://localhost:8080/api/test
  // =>
  // http://localhost:8080/test
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        // target: 'http://192.168.2.7:8000',
        // target: 'http://django.t.mukewang.com',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''   //需要rewrite重写的url
        }
      }
    }
  }
})
