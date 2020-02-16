function showToast(title, icon) {
  wx.showToast({
    title: title,
    icon: icon
  })
}

function showToast2(icon){
  wx.showToast({
    title: "信息修改成功",
    icon: icon
  })
}

function showToast3() {
  wx.showToast({
    title: "登陆失败请重试",
  })
}

module.exports = {
  showToast: showToast,
  showToast2:showToast2,
  showToast3: showToast3
}