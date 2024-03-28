const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
  // devServer:{
  //   port:80
  // }
})
const cors = require('cors')  
  
module.exports = {  
  devServer: {  
    before: cors(),  
  },  
}
