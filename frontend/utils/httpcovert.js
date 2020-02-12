
function Httpcovert(t){
  console.log("kankan", t)
  if (t.length > 0) {
    var x;
    var convertedarr = [];
    var convertobject = {};
    for (x in t) {
      wx.downloadFile({
        url: t[x],
        success(res) {
          convertobject['path'] = t[x]
          wx.getFileSystemManager().readFile({
            filePath: res.tempFilePath, //选择图片返回的相对路径
            encoding: 'base64', //编码格式
            success: res => { //成功的回调
              console.log('data:image/png;base64,' + res.data)
              convertobject['base64'] = res.data
            }
          })
        }
      })
      convertedarr.push(convertobject)
      console.log(convertedarr)
    }
  }
  return convertedarr
}

module.exports = {
  httpcovert: Httpcovert
  }
