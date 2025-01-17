//index.js
//获取应用实例
const app = getApp()
var Request = require("../../utils/request.js");
var Api = require("../../api/api.js");
var UploadImage = require("../../utils/uploadimage.js");
var thatDate = require("../../utils/thatdate.js");
var showToast = require("../../utils/showToast.js");
var UpImages = require("../../utils/UpImages.js");
var Re = require("../../utils/re.js")

Page({
  /**
  * 页面的初始数据
  */
  data: {

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    if (!app.globalData.jwt) {
      wx.redirectTo({
        url: '../login/login',
      })
    }
    // 获取个人信息
    Request.request(Api.GetUser, '', 'GET')
      .then(function (res) {
        //console.log("shabi",res)
        if (res.data.detail == "Signature has expired.") {
          console.log("redirect", res.data.detail)
          app.globalData.jwt = null;
          wx.redirectTo({
            url: '../login/login',

          })
        } else {
          that.setData(res.data)
        }
      })
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
    this.onLoad()
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
  // onShareAppMessage: function () {

  // }
  // 更换背景和更换头像
  huanbeijing: function (event) {
    var that = this
    var types = event.currentTarget.dataset.type
    //选着照片
    var that = this
    UploadImage.uploadImage(1)
      .then(function (image_path) {
        UpImages.UpImages(Api.GetUser, image_path.tempFilePaths[0], {
          'types': types
        })
          .then(function (res) {
            if (res.statusCode == 200) {
              //console.log(res)
              showToast.showToast('更换成功', 'success')
              setTimeout(function () {
                that.onLoad()
              }, 500)
            } else {
              showToast.showToast('更换失败', 'success')
            }
          })
      })
  },
  // 点击我的信息跳转
  wodexinxi: function () {
    wx.navigateTo({
      url: './userinfo/userinfo',
    })
  },
  // 点击我的会议跳转
  wofabude: function () {
    wx.navigateTo({
      url: './meeting/meeting',
    })
  },
  // 点击打卡记录的跳转
  liulanjilu: function () {
    wx.navigateTo({
      url: './record/record',
    })
  },
  // 点击打卡记录的跳转
  collection: function () {
    wx.navigateTo({
      url: './xuexi/xuexi',
    })
  },
  // 点击打卡记录的跳转
  wodebaoming: function () {
    wx.navigateTo({
      url: './rank/rank',
    })
  },
  // 点击打卡记录的跳转
  Advicefeedback: function () {
    wx.navigateTo({
      url: './advice/advice',
    })
  },


})
