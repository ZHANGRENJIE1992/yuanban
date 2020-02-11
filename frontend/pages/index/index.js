//index.js
//获取应用实例
const app = getApp()
var Api = require("../../api/api.js")
var Request = require("../../utils/request.js");
var reconstructionArray = require("../../utils/reconstructionArray.js")
var all_data_list = ''
var ActivityType_list = ''
var timer = null


Page({
  data: {
    view_hidden: true,
    SlideImage: '',
    startDateList: '',
    clientHeight: 0,
    startDateListis: true,
    ActivityTypeis: true,
    Registration_datais: true,
    all_datais: true,
    //motto: 'Hello World',
    //userInfo: {},
    //hasUserInfo: false,
    //canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function (options) {
    var that = this;
    if (!app.globalData.jwt) {
      wx.redirectTo({
        url: '../login/login',
      })
      return false
    }

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    var that = this
    setTimeout(function () {
      that.setData({
        view_hidden: '',
      })
    }, 500)
  },


  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    var that = this;
    if (!app.globalData.jwt) {
      wx.redirectTo({
        url: '../login/login',
      })
      return false
    } else {
      console.log(11)
    }
  },

  /**
 * 生命周期函数--监听页面隐藏
 */
  onHide: function () {
    clearInterval(timer);
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
    // wx.showNavigationBarLoading() //在标题栏中显示加载
    this.onLoad()
    clearInterval(timer);
    this.onShow()
    setTimeout(function () {
      // complete
      wx.hideNavigationBarLoading() //完成停止加载
      wx.stopPullDownRefresh() //停止下拉刷新
    }, 1500);
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },
  // // 上拉加载更多
  // loadMore: function () {
  //   console.log('11111111111')
  // },
  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {
    var that = this;
    var sharedata = reconstructionArray.getRandomArrayElements(that.data.sharing, 1)[0]
    return {
      title: sharedata.title,
      path: 'pages/signdaily/signdaily',
      imageUrl: sharedata.imageUrl,
      success(e) {
        wx.showShareMenu({
          withShareTicket: true
        })
        // 获取分享用户
        Request.request(Api.SharingUserViewSet, '', 'POST')
          .then(function(res) {
            console.LOG(res)
          })
      }
    }
  },

  // 点击yasi跳转
  yasi: function () {
    wx.navigateTo({
      url: './ielts/ielts',
    })
  },

  // 点击tuofu跳转
  tuofu: function () {
    wx.navigateTo({
      url: './toefl/toefl',
    })
  },

  // 点击gre跳转
  gre: function () {
    wx.navigateTo({
      url: './gre/gre',
    })
  },

  // 点击gmat跳转
  gmat: function () {
    wx.navigateTo({
      url: './gmat/gmat',
    })
  },
})

