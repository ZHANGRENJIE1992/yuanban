// pages/index/ielts/ielts.js
var upFiles = require('../../../utils/upFiles.js')
var Re = require("../../../utils/re.js");
var Request = require("../../../utils/request.js");
var Api = require("../../../api/api.js")

const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    dancihiddeninput: true,
    readhiddeninput: true,
    grammarhiddeninput: true,
    logichiddeninput: true,
    mathhiddeninput: true,
    upFilesBtn: true,
    upFilesProgress: false,
    riqi_STR: ['今天', '昨天', '前天'],
    riqi_index: 0,
    maxUploadLen: 6,
    word_index: 5,
    read_index: 7,
    write_index: 10,
    grammar_index: 6,
    math_index: 9,
    logic_index: 8,
    upImgArr_gmat_word: [],
    upImgArr_gmat_read: [],
    upImgArr_gmat_write: [],
    upImgArr_gmat_grammar: [],
    upImgArr_gmat_math: [],
    upImgArr_gmat_logic: [],
    new_danci: null,
    new_read: null,
    new_grammar: null,
    new_logic: null,
    new_math: null,
    username: null
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 获取个人信息
    var _this = this
    Request.request(Api.GetUser, '', 'GET')
      .then(function (res) {
        //console.log(res)
        //that.setData(res.data)
        _this.data.username = res.data.username
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
    let arr = _this.data.upImgArr;
    let preArr = [];
    arr.map(function (v, i) {
      preArr.push(v.path)
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
          let upVideoArr = _this.data.upVideoArr;
          if (delType == 'image') {
            upImgArr.splice(delNum, 1)
            _this.setData({
              upImgArr: upImgArr,
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
    let arr_read = _this.data.upImgArr_read;
    let preArr_read = [];
    arr_read.map(function (v, i) {
      preArr_read.push(v.path)
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
          //let upVideoArr = _this.data.upVideoArr;
          if (delType == 'image') {
            upImgArr_read.splice(delNum, 1)
            _this.setData({
              upImgArr_read: upImgArr_read,
            })
          }
          let upFilesArr_read = upFiles.getPathArr(_this);
          if (upFilesArr_read.length < _this.data.maxUploadLen) {
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
  previewImg_write: function (e) {
    let imgsrc_write = e.currentTarget.dataset.presrc;
    let _this = this;
    let arr_write = _this.data.upImgArr_write;
    let preArr_write = [];
    arr_write.map(function (v, i) {
      preArr_write.push(v.path)
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
          if (delType == 'image') {
            upImgArr_write.splice(delNum, 1)
            _this.setData({
              upImgArr_write: upImgArr_write,
            })
          }
          let upFilesArr_write = upFiles.getPathArr(_this);
          if (upFilesArr_write.length < _this.data.maxUploadLen) {
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
  previewImg_grammar: function (e) {
    let imgsrc_grammar = e.currentTarget.dataset.presrc;
    let _this = this;
    let arr_grammar = _this.data.upImgArr_grammar;
    let preArr_grammar = [];
    arr_grammar.map(function (v, i) {
      preArr_grammar.push(v.path)
    })
    //   console.log(preArr)
    wx.previewImage({
      current: imgsrc_grammar,
      urls: preArr_grammar
    })
  },
  // 删除上传图片 或者视频
  delFile_grammar: function (e) {
    let _this = this;
    wx.showModal({
      title: '提示',
      content: '您确认删除嘛？',
      success: function (res) {
        if (res.confirm) {
          let delNum = e.currentTarget.dataset.index;
          let delType = e.currentTarget.dataset.type;
          let upImgArr_grammar = _this.data.upImgArr_grammar;
          if (delType == 'image') {
            upImgArr_grammar.splice(delNum, 1)
            _this.setData({
              upImgArr_grammar: upImgArr_grammar,
            })
          }
          let upFilesArr_grammar = upFiles.getPathArr(_this);
          if (upFilesArr_grammar.length < _this.data.maxUploadLen) {
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
  previewImg_math: function (e) {
    let imgsrc_math = e.currentTarget.dataset.presrc;
    let _this = this;
    let arr_math = _this.data.upImgArr_math;
    let preArr_math = [];
    arr_math.map(function (v, i) {
      preArr_math.push(v.path)
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
          if (delType == 'image') {
            upImgArr_math.splice(delNum, 1)
            _this.setData({
              upImgArr_math: upImgArr_math,
            })
          }
          let upFilesArr_math = upFiles.getPathArr(_this);
          if (upFilesArr_math.length < _this.data.maxUploadLen) {
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
  previewImg_logic: function (e) {
    let imgsrc_logic = e.currentTarget.dataset.presrc;
    let _this = this;
    let arr_logic = _this.data.upImgArr_logic;
    let preArr_logic = [];
    arr_logic.map(function (v, i) {
      preArr_logic.push(v.path)
    })
    //   console.log(preArr)
    wx.previewImage({
      current: imgsrc_logic,
      urls: preArr_logic
    })
  },
  // 删除上传图片 或者视频
  delFile_logic: function (e) {
    let _this = this;
    wx.showModal({
      title: '提示',
      content: '您确认删除嘛？',
      success: function (res) {
        if (res.confirm) {
          let delNum = e.currentTarget.dataset.index;
          let delType = e.currentTarget.dataset.type;
          let upImgArr_logic = _this.data.upImgArr_logic;
          if (delType == 'image') {
            upImgArr_logic.splice(delNum, 1)
            _this.setData({
              upImgArr_logic: upImgArr_logic,
            })
          }
          let upFilesArr_logic = upFiles.getPathArr(_this);
          if (upFilesArr_logic.length < _this.data.maxUploadLen) {
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

  riqi: function (e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      riqi_index: e.detail.value,
      date: e.detail.value
    })
  },
  // 选择图片或者视频单词
  uploadFiles: function (e) {
    var _this = this;
    var uploadindex = e.currentTarget.dataset.upload;
    console.log("shabi", e.currentTarget.dataset.upload)
    upFiles.chooseImage(_this, _this.data.maxUploadLen, uploadindex)
  },


  // 选择图片或者视频
  uploadFiles_write: function (e) {
    var _this = this;
    //   console.log(res.tapIndex)
    upFiles.chooseImage(_this, _this.data.maxUploadLen)
  },


  // 选择图片或者视频
  uploadFiles_listen: function (e) {
    var _this = this;
    //   console.log(res.tapIndex)
    upFiles.chooseImage(_this, _this.data.maxUploadLen)
  },


  // 选择图片或者视频
  uploadFiles_speak: function (e) {
    var _this = this;
    //   console.log(res.tapIndex)
    upFiles.chooseImage(_this, _this.data.maxUploadLen)
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
  new_listens: function (event) {
    var that = this
    var new_listen = event.detail.value
    if (new_listen > 100) {
      new_listen = 100
    } else if (new_listen.indexOf(" ") != -1) {
      new_listen = null
    }
    that.setData({
      new_listen: new_listen
    })
  },
  listen_number: function () {
    var that = this
    that.setData({
      listenhiddeninput: false,
    })
  },
  cancellisten: function () {
    var that = this
    that.setData({
      listenhiddeninput: true,
    })
  },
  confirmlisten: function (e) {
    var that = this
    var new_listen = that.data.new_listen
    that.setData({
      listenhiddeninput: true,
    })
  },
  subFormData: function () {
    var _this = this
    console.log(_this.data)
    Request.request(Api.Ieltssubmitinfo, _this.data, 'POST').then(function (res) {
      if (res.statusCode == 200) {
        console.log("ielts success!")
      }
      _this.onLoad()
    })

  }
})