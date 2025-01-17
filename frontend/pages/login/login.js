// pages/login/login.js
const app = getApp()
var Api = require("../../api/api.js")
var Request = require("../../utils/request.js");
var reconstructionArray = require("../../utils/reconstructionArray.js")
var timer = ''

var content = "在您使用本软件的同时，请认真且时刻遵守法律法规"

Page({

  /**
   * 页面的初始数据
   */
  data: {
    disabled: true,
    num:0
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    //console.log("login",app.globalData.jwt)
    if (app.globalData.jwt) {
      wx.switchTab({
        url: '../index/index',
      })
    }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    var that = this
    // 获取注册页面分享数据
    /*Request.request(Api.GeneralSharingViewSet, '', 'GET')
      .then(function (res) {
        that.setData({
          gensharing: res.data
        })
      })
    //console.log(that.data)
    timer = setInterval(this.onLoad, 2000)*/
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    clearInterval(timer);
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    var that = this;
    var sharedata = reconstructionArray.getRandomArrayElements(that.data.gensharing, 1)[0]
    return {
      title: sharedata.title,
      path: 'pages/index/index',
      imageUrl: sharedata.imageUrl,
    }
  },
  agreeGetUser: function (e) {
    var that = this;
    that.setData({
      disabled: true,
    })
    app.login(e);
  },
  checkboxChange: function (e) {
    var that = this;

    if (that.data.num == 0) {
      that.setData({
        disabled: false,
        num:1,
      })
      return false
    } else {
      that.setData({
        disabled: true,
        num: 0
      })
      return false
    }
  },
  // 点击阅读协议
  yuedu: function () {
    var that = this
    wx.showModal({
      title: '使用协议',
      content: content,
      showCancel: false,
      confirmText: '我已阅读',
      confirmColor: '#eb4901'
    })
  }
})