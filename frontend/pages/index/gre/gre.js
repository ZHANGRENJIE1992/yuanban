// pages/index/ielts/ielts.js
var upFiles = require('../../../utils/upFiles.js')
var Re = require("../../../utils/re.js");
var Request = require("../../../utils/request.js");
var Api = require("../../../api/api.js")
var Httpcovert = require("../../../utils/httpcovert.js")
var Format = require("../../../utils/datetime.js")

const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    dancihiddeninput: true,
    readhiddeninput: true,
    mathhiddeninput: true,
    blankhiddeninput: true,
    upFilesBtn: true,
    upFilesProgress: false,
    riqi_STR: ['今天', '昨天', '前天'],
    riqi_index: 0,
    maxUploadLen: 6,
    word_index: 0,
    read_index: 1,
    write_index: 2,
    blank_index: 5,
    math_index: 6,
    upImgArr: [],
    upImgArr_read: [],
    upImgArr_write: [],
    upImgArr_blank: [],
    upImgArr_math: [],
    path_upImgArr: [],
    path_upImgArr_read: [],
    path_upImgArr_write: [],
    path_upImgArr_blank: [],
    path_upImgArr_math: [], 
    new_danci: null,
    new_blank: null,
    new_read: null,
    new_math: null,
    username: null
  },

  /**
     * 生命周期函数--监听页面加载
     */
  onLoad: function (options) {
    // 获取个人信息
    if (!app.globalData.jwt) {
      wx.redirectTo({
        url: '../login/login',
      })
    }
    var _this = this
    console.log("载入查看", options)
    var arr = Object.keys(options);
    if (arr.length == 0) {
      options = new Date()
      options = options.getFullYear() + "-" + (options.getMonth() + 1) + "-" + options.getDate();
      _this.data.s = options
    }
    Request.request(Api.Gregetinfo, { date: options }, 'GET').then(function (res) {
      if (res.statusCode !== 204) {
        console.log("载入成功row", res.data)
        _this.data.path_upImgArr = res.data.upImgArr
        _this.data.path_upImgArr_read = res.data.upImgArr_read
        _this.data.path_upImgArr_write = res.data.upImgArr_write
        _this.data.path_upImgArr_blank = res.data.upImgArr_blank
        _this.data.path_upImgArr_math = res.data.upImgArr_math
        _this.data.new_danci = res.data.new_danci
        _this.data.new_read = res.data.new_read
        _this.data.new_blank = res.data.new_blank
        _this.data.new_math = res.data.new_math

        _this.setData(_this.data)
        _this.data.upImgArr = Httpcovert.httpcovert(res.data.upImgArr)
        _this.data.upImgArr_math = Httpcovert.httpcovert(res.data.upImgArr_math)
        _this.data.upImgArr_read = Httpcovert.httpcovert(res.data.upImgArr_read)
        _this.data.upImgArr_blank = Httpcovert.httpcovert(res.data.upImgArr_blank)
        _this.data.upImgArr_write = Httpcovert.httpcovert(res.data.upImgArr_write)


        console.log("载入处理后", _this.data)
      }
    })
    _this.data.loadfinish = true
    _this.setData(_this.data.loadfinish)
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
  onShareAppMessage: function () {

  },


  // 预览图片
  previewImg: function (e) {
    let imgsrc = e.currentTarget.dataset.presrc;
    let _this = this;
    let arr = _this.data.path_upImgArr;
    let preArr = [];
    arr.map(function (v, i) {
      preArr.push(v)
    })
    //   console.log(preArr)
    wx.previewImage({
      current: imgsrc,
      urls: preArr
    })
  },
  // 删除上传图片 或者视频
  delFile: function (e) {
    let _this = this;
    wx.showModal({
      title: '提示',
      content: '您确认删除嘛？',
      success: function (res) {
        if (res.confirm) {
          let delNum = e.currentTarget.dataset.index;
          let delType = e.currentTarget.dataset.type;
          let upImgArr = _this.data.upImgArr;
          let path_upImgArr = _this.data.path_upImgArr;
          if (delType == 'image') {
            upImgArr.splice(delNum, 1)
            path_upImgArr.splice(delNum, 1)
            _this.setData({
              upImgArr: upImgArr,
            })
            _this.setData({
              path_upImgArr: path_upImgArr,
            })
          } else if (delType == 'video') {
            upVideoArr.splice(delNum, 1)
            _this.setData({
              upVideoArr: upVideoArr,
            })
          }
          let upFilesArr = upFiles.getPathArr(_this);
          if (upFilesArr.length < _this.data.maxUploadLen) {
            _this.setData({
              upFilesBtn: true,
            })
          }
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  // 预览图片
  previewImg_read: function (e) {
    let imgsrc_read = e.currentTarget.dataset.presrc;
    let _this = this;
    let arr_read = _this.data.path_upImgArr_read;
    let preArr_read = [];
    arr_read.map(function (v, i) {
      preArr_read.push(v)
    })
    //   console.log(preArr)
    wx.previewImage({
      current: imgsrc_read,
      urls: preArr_read
    })
  },
  // 删除上传图片 或者视频
  delFile_read: function (e) {
    let _this = this;
    wx.showModal({
      title: '提示',
      content: '您确认删除嘛？',
      success: function (res) {
        if (res.confirm) {
          let delNum = e.currentTarget.dataset.index;
          let delType = e.currentTarget.dataset.type;
          let upImgArr_read = _this.data.upImgArr_read;
          let path_upImgArr_read = _this.data.path_upImgArr_read;
          //let upVideoArr = _this.data.upVideoArr;
          if (delType == 'image') {
            upImgArr_read.splice(delNum, 1)
            path_upImgArr_read.splice(delNum, 1)
            _this.setData({
              upImgArr_read: upImgArr_read,
              path_upImgArr_read: path_upImgArr_read,
            })
          }
          let upFilesArr_read = upFiles.getPathArr(_this);
          if (upFilesArr_read.length < _this.data.maxUploadLen) {
            _this.setData({
              upFilesBtn_read: true,
            })
          }
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  // 预览图片
  previewImg_write: function (e) {
    let imgsrc_write = e.currentTarget.dataset.presrc;
    let _this = this;
    let arr_write = _this.data.path_upImgArr_write;
    let preArr_write = [];
    arr_write.map(function (v, i) {
      preArr_write.push(v)
    })
    //   console.log(preArr)
    wx.previewImage({
      current: imgsrc_write,
      urls: preArr_write
    })
  },
  // 删除上传图片 或者视频
  delFile_write: function (e) {
    let _this = this;
    wx.showModal({
      title: '提示',
      content: '您确认删除嘛？',
      success: function (res) {
        if (res.confirm) {
          let delNum = e.currentTarget.dataset.index;
          let delType = e.currentTarget.dataset.type;
          let upImgArr_write = _this.data.upImgArr_write;
          let path_upImgArr_write = _this.data.path_upImgArr_write
          if (delType == 'image') {
            upImgArr_write.splice(delNum, 1)
            path_upImgArr_write.splice(delNum, 1)
            _this.setData({
              upImgArr_write: upImgArr_write,
              path_upImgArr_write: path_upImgArr_write,
            })
          }
          let upFilesArr_write = upFiles.getPathArr(_this);
          if (upFilesArr_write.length < _this.data.maxUploadLen) {
            _this.setData({
              upFilesBtn_write: true,
            })
          }
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  // 预览图片
  previewImg_blank: function (e) {
    let imgsrc_blank = e.currentTarget.dataset.presrc;
    let _this = this;
    let arr_blank = _this.data.path_upImgArr_blank;
    let preArr_blank = [];
    arr_blank.map(function (v, i) {
      preArr_blank.push(v)
    })
    //   console.log(preArr)
    wx.previewImage({
      current: imgsrc_blank,
      urls: preArr_blank
    })
  },
  // 删除上传图片 或者视频
  delFile_blank: function (e) {
    let _this = this;
    wx.showModal({
      title: '提示',
      content: '您确认删除嘛？',
      success: function (res) {
        if (res.confirm) {
          let delNum = e.currentTarget.dataset.index;
          let delType = e.currentTarget.dataset.type;
          let upImgArr_blank = _this.data.upImgArr_blank;
          let path_upImgArr_blank = _this.data.path_upImgArr_blank;
          if (delType == 'image') {
            upImgArr_blank.splice(delNum, 1)
            path_upImgArr_blank.splice(delNum, 1)
            _this.setData({
              upImgArr_blank: upImgArr_blank,
              path_upImgArr_blank: path_upImgArr_blank,
            })
          }
          let upFilesArr_blank = upFiles.getPathArr(_this);
          if (upFilesArr_blank.length < _this.data.maxUploadLen) {
            _this.setData({
              upFilesBtn_blank: true,
            })
          }
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  // 预览图片
  previewImg_math: function (e) {
    let imgsrc_math = e.currentTarget.dataset.presrc;
    let _this = this;
    let arr_math = _this.data.pathupImgArr_math;
    let preArr_math = [];
    arr_math.map(function (v, i) {
      preArr_math.push(v)
    })
    //   console.log(preArr)
    wx.previewImage({
      current: imgsrc_math,
      urls: preArr_math
    })
  },
  // 删除上传图片 或者视频
  delFile_math: function (e) {
    let _this = this;
    wx.showModal({
      title: '提示',
      content: '您确认删除嘛？',
      success: function (res) {
        if (res.confirm) {
          let delNum = e.currentTarget.dataset.index;
          let delType = e.currentTarget.dataset.type;
          let upImgArr_math = _this.data.upImgArr_math;
          let path_upImgArr_math = _this.data.path_upImgArr_math;
          if (delType == 'image') {
            upImgArr_math.splice(delNum, 1)
            path_upImgArr_math.splice(delNum, 1)
            _this.setData({
              upImgArr_math: upImgArr_math,
              path_upImgArr_math: path_upImgArr_math
            })
          }
          let upFilesArr_math = upFiles.getPathArr(_this);
          if (upFilesArr_math.length < _this.data.maxUploadLen) {
            _this.setData({
              upFilesBtn_math: true,
            })
          }
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },

  riqi: function (e) {
    var _this = this
    var requestdata = {}

    if (e.detail.value === "0") {

      var today = new Date();
      today.setTime(today.getTime());
      var s1 = today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
      requestdata['date'] = s1
      _this.setData({
        s: s1,
      })
      console.log('picker发送选择改变，携带值为', requestdata)
      Request.request(Api.Gregetinfo, requestdata, 'GET').then(function (res) {
        if (res.statusCode !== 204) {
          console.log("载入成功row", res.data)
          _this.data.path_upImgArr = res.data.upImgArr
          _this.data.path_upImgArr_read = res.data.upImgArr_read
          _this.data.path_upImgArr_write = res.data.upImgArr_write
          _this.data.path_upImgArr_blank = res.data.upImgArr_blank
          _this.data.path_upImgArr_math = res.data.upImgArr_math
          _this.data.new_danci = res.data.new_danci
          _this.data.new_read = res.data.new_read
          _this.data.new_blank = res.data.new_blank
          _this.data.new_math = res.data.new_math

          _this.setData(_this.data)
          _this.data.upImgArr = Httpcovert.httpcovert(res.data.upImgArr)
          _this.data.upImgArr_math = Httpcovert.httpcovert(res.data.upImgArr_math)
          _this.data.upImgArr_read = Httpcovert.httpcovert(res.data.upImgArr_read)
          _this.data.upImgArr_blank = Httpcovert.httpcovert(res.data.upImgArr_blank)
          _this.data.upImgArr_write = Httpcovert.httpcovert(res.data.upImgArr_write)


          console.log("载入处理后", _this.data)
        } else {
          var tempdata = {
            riqi_index: 0,
            upImgArr: [],
            upImgArr_read: [],
            upImgArr_write: [],
            upImgArr_math: [],
            upImgArr_blank: [],
            path_upImgArr: [],
            path_upImgArr_read: [],
            path_upImgArr_write: [],
            path_upImgArr_math: [],
            path_upImgArr_blank: [],
            new_danci: null,
            new_read: null,
            new_math: null,
            new_blank: null,
            username: null,
            s: s1
          }
          _this.setData(tempdata)
        }

      })

    }
    if (e.detail.value === "1") {
      var yesterday = new Date();
      var s2 = yesterday.getFullYear() + "-" + (yesterday.getMonth() + 1) + "-" + (yesterday.getDate() - 1);
      requestdata['date'] = s2
      _this.setData({
        s: s2,
      })
      Request.request(Api.Gregetinfo, requestdata, 'GET').then(function (res) {
        if (res.statusCode !== 204) {
          console.log("载入成功row", res.data)
          _this.data.path_upImgArr = res.data.upImgArr
          _this.data.path_upImgArr_read = res.data.upImgArr_read
          _this.data.path_upImgArr_write = res.data.upImgArr_write
          _this.data.path_upImgArr_blank = res.data.upImgArr_blank
          _this.data.path_upImgArr_math = res.data.upImgArr_math
          _this.data.new_danci = res.data.new_danci
          _this.data.new_read = res.data.new_read
          _this.data.new_blank = res.data.new_blank
          _this.data.new_math = res.data.new_math

          _this.setData(_this.data)
          _this.data.upImgArr = Httpcovert.httpcovert(res.data.upImgArr)
          _this.data.upImgArr_math = Httpcovert.httpcovert(res.data.upImgArr_math)
          _this.data.upImgArr_read = Httpcovert.httpcovert(res.data.upImgArr_read)
          _this.data.upImgArr_blank = Httpcovert.httpcovert(res.data.upImgArr_blank)
          _this.data.upImgArr_write = Httpcovert.httpcovert(res.data.upImgArr_write)


          console.log("载入处理后", _this.data)
        } else {
          var tempdata = {
            riqi_index: 1,
            upImgArr: [],
            upImgArr_read: [],
            upImgArr_write: [],
            upImgArr_math: [],
            upImgArr_blank: [],
            path_upImgArr: [],
            path_upImgArr_read: [],
            path_upImgArr_write: [],
            path_upImgArr_math: [],
            path_upImgArr_blank: [],
            new_danci: null,
            new_read: null,
            new_math: null,
            new_blank: null,
            username: null,
            s: s2
          }
          _this.setData(tempdata)
        }
      })

    }
    if (e.detail.value === "2") {
      var twodaysbefore = new Date();
      var s3 = twodaysbefore.getFullYear() + "-" + (twodaysbefore.getMonth() + 1) + "-" + (twodaysbefore.getDate() - 2);
      _this.setData({
        s: s3,
      })
      Request.request(Api.Gregetinfo, {
        date: s3
      }, 'GET').then(function (res) {
        if (res.statusCode !== 204) {
          console.log("载入成功row", res.data)
          _this.data.path_upImgArr = res.data.upImgArr
          _this.data.path_upImgArr_read = res.data.upImgArr_read
          _this.data.path_upImgArr_write = res.data.upImgArr_write
          _this.data.path_upImgArr_blank = res.data.upImgArr_blank
          _this.data.path_upImgArr_math = res.data.upImgArr_math
          _this.data.new_danci = res.data.new_danci
          _this.data.new_read = res.data.new_read
          _this.data.new_blank = res.data.new_blank
          _this.data.new_math = res.data.new_math

          _this.setData(_this.data)
          _this.data.upImgArr = Httpcovert.httpcovert(res.data.upImgArr)
          _this.data.upImgArr_math = Httpcovert.httpcovert(res.data.upImgArr_math)
          _this.data.upImgArr_read = Httpcovert.httpcovert(res.data.upImgArr_read)
          _this.data.upImgArr_blank = Httpcovert.httpcovert(res.data.upImgArr_blank)
          _this.data.upImgArr_write = Httpcovert.httpcovert(res.data.upImgArr_write)


          console.log("载入处理后", _this.data)
        } else {
          var tempdata = {
            riqi_index: 2,
            upImgArr: [],
            upImgArr_read: [],
            upImgArr_write: [],
            upImgArr_math: [],
            upImgArr_blank: [],
            path_upImgArr: [],
            path_upImgArr_read: [],
            path_upImgArr_write: [],
            path_upImgArr_math: [],
            path_upImgArr_blank: [],
            new_danci: null,
            new_read: null,
            new_math: null,
            new_blank: null,
            username: null,
            s: s3
          }
          _this.setData(tempdata)
        }
      })
    }

    _this.setData({
      riqi_index: e.detail.value,
      date: e.detail.value
    })
  },

  // 选择图片或者视频单词
  uploadFiles: function (e) {
    var _this = this;
    var uploadindex = e.currentTarget.dataset.upload;

    upFiles.chooseImage(_this, _this.data.maxUploadLen, uploadindex)
  },

  new_dancis: function (event) {
    var that = this
    var new_danci = event.detail.value
    if (new_danci.indexOf(" ") != -1) {
      new_danci = null
    }
    that.setData({
      new_danci: new_danci
    })
  },
  danci_number: function () {
    var that = this
    that.setData({
      dancihiddeninput: false,
    })
  },
  canceldanci: function () {
    var that = this
    that.setData({
      dancihiddeninput: true,
    })
  },
  confirmdanci: function (e) {
    var that = this
    var new_danci = that.data.new_danci
    that.setData({
      dancihiddeninput: true,
    })
  },
  new_blank: function (event) {
    var that = this
    var new_blank = event.detail.value
    if (new_blank.indexOf(" ") != -1) {
      new_blank = null
    }
    that.setData({
      new_blank: new_blank
    })
  },
  blank_number: function () {
    var that = this
    that.setData({
      blankhiddeninput: false,
    })
  },
  cancelblank: function () {
    var that = this
    that.setData({
      blankhiddeninput: true,
    })
  },
  confirmblank: function (e) {
    var that = this
    var new_blank = that.data.new_blank
    that.setData({
      blankhiddeninput: true,
    })
  },
  new_reads: function (event) {
    var that = this
    var new_read = event.detail.value
    if (new_read > 100) {
      new_read = 100
    } else if (new_read.indexOf(" ") != -1) {
      new_read = null
    }
    that.setData({
      new_read: new_read
    })
  },
  read_number: function () {
    var that = this
    that.setData({
      readhiddeninput: false,
    })
  },
  cancelread: function () {
    var that = this
    that.setData({
      readhiddeninput: true,
    })
  },
  confirmread: function (e) {
    var that = this
    var new_read = that.data.new_read
    that.setData({
      readhiddeninput: true,
    })
  },
  new_math: function (event) {
    var that = this
    var new_math = event.detail.value
    if (new_math > 100) {
      new_math = 100
    } else if (new_math.indexOf(" ") != -1) {
      new_math = null
    }
    that.setData({
      new_math: new_math
    })
  },
  math_number: function () {
    var that = this
    that.setData({
      mathhiddeninput: false,
    })
  },
  cancelmath: function () {
    var that = this
    that.setData({
      mathhiddeninput: true,
    })
  },
  confirmmath: function (e) {
    var that = this
    var new_math = that.data.new_math
    that.setData({
      mathhiddeninput: true,
    })
  },
  subFormData: function () {
    var _this = this
    if (_this.data.new_danci === null) {
      _this.data.new_danci = 0
    }
    if (_this.data.new_math === null) {
      _this.data.new_math = 0
    }
    if (_this.data.new_read === null) {
      _this.data.new_read = 0
    }
    if (_this.data.new_blank === null) {
      _this.data.new_blank = 0
    }
    console.log("提交时日期", _this.data)
    Request.request(Api.Gresubmitinfo, _this.data, 'POST').then(function (res) {
      if (res.statusCode == 200) {
        console.log("ielts success!")
      }
      _this.onLoad(_this.data.s)
    })

  },
})