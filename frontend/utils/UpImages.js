const app = getApp()

function UpImages(url, data, formData) {
  var get_data = new Promise(function(resolve, reject) {
    console.log('url',url),
    console.log('data',data),
    wx.uploadFile({
      url: url,
      filePath: data,
      name: 'file',
      header: {
        'Authorization': 'JWT ' + app.globalData.jwt,
        'Content-Type': 'multipart/form-data'
      },
      formData: formData,
      success: resolve
    })
  })
  return get_data
}

module.exports = {
  UpImages: UpImages
}