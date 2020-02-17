
var chooseImage = (t, count, uploadindex) =>{
    wx.chooseImage({
        count: count,
        sizeType: ['original', 'compressed'],
        sourceType: ['album', 'camera'],
          success: (res) => {
            if (uploadindex == 0){
              var imgArr = t.data.upImgArr || [];
              let arr = res.tempFiles;
              var temppath_imgArr = t.data.path_upImgArr || [];
              var i =0;
              for(i in arr){
                temppath_imgArr.push(arr[i]['path'])
              }

              //console.log(t)
              arr.map(function(v,i){
                  wx.getFileSystemManager().readFile({
                    filePath: res.tempFilePaths[i], //选择图片返回的相对路径
                    encoding: 'base64', //编码格式
                    success: res => { //成功的回调
                      //console.log('data:image/png;base64,' + res.data)
                      v['base64'] = res.data;
                    }
                  })
                  v['progress'] = 0;               
                  imgArr.push(v)
                 
              })
              t.data.upImgArr = imgArr
              t.setData({
                  path_upImgArr: temppath_imgArr
              })
              //console.log("111", imgArr)
              let upFilesArr = getPathArr(t);
              if (upFilesArr.length > count-1) {
                  let imgArr = t.data.upImgArr;
                  let newimgArr = imgArr.slice(0, count)
                  t.setData({
                      upFilesBtn: false,
                      upImgArr: newimgArr
                  })
              }
            }
            if (uploadindex == 1) {
              var imgArr_read = t.data.upImgArr_read || [];
              let arr_read = res.tempFiles;
              var temppath_imgArr_read = t.data.path_upImgArr_read || [];
              var i = 0;
              //console.log(1, temppath_imgArr)
              for (i in arr_read) {
                temppath_imgArr_read.push(arr_read[i]['path'])
              }
              //console.log(res)
              //console.log("imgArr_read是啥", t.data.upImgArr_read)
              arr_read.map(function (v, i) {
                wx.getFileSystemManager().readFile({
                  filePath: res.tempFilePaths[0], //选择图片返回的相对路径
                  encoding: 'base64', //编码格式
                  success: res => { //成功的回调
                    //console.log('data:image/png;base64,' + res.data)
                    v['base64'] = res.data;
                  }
                })
                v['progress'] = 0;
                imgArr_read.push(v)
              })
              //console.log("阅读图片集", temppath_imgArr_read)
              t.data.upImgArr_read = imgArr_read
              t.setData({      
                path_upImgArr_read: temppath_imgArr_read
              })
              let upFilesArr_read = getPathArr_ielts_read(t);
              if (upFilesArr_read.length > count - 1) {
                let imgArr_read = t.data.upImgArr_read;
                let newimgArr_read = imgArr_read.slice(0, count)
                t.setData({
                  upFilesBtn_read: false,
                  upImgArr_read: newimgArr_read
                })
              }
            }
            if (uploadindex == 2) {
              var imgArr_write = t.data.upImgArr_write || [];
              let arr_write = res.tempFiles;
              var temppath_imgArr_write = t.data.path_upImgArr_write || [];
              var i = 0;
              //console.log(1, temppath_imgArr)
              for (i in arr_write) {
                temppath_imgArr_write.push(arr_write[i]['path'])
              }
              //console.log("原始write", t.data.upImgArr_write)
              //console.log(t)
              arr_write.map(function (v, i) {
                wx.getFileSystemManager().readFile({
                  filePath: res.tempFilePaths[i], //选择图片返回的相对路径
                  encoding: 'base64', //编码格式
                  success: res => { //成功的回调
                    //console.log('data:image/png;base64,' + res.data)
                    v['base64'] = res.data;
                  }
                })
                v['progress'] = 0;
                imgArr_write.push(v)
              })
              t.data.upImgArr_write = imgArr_write
              //console.log("write:", imgArr_write)
              t.setData({
                path_upImgArr_write: temppath_imgArr_write

              })

              let upFilesArr_write = getPathArr_ielts_write(t);
              if (upFilesArr_write.length > count - 1) {
                let imgArr_write = t.data.upImgArr_write;
                let newimgArr_write = imgArr_write.slice(0, count)
                t.setData({
                  upFilesBtn_write: false,
                  upImgArr_write: newimgArr_write
                })
              }
            }
            if (uploadindex == 3) {
              var imgArr_listen = t.data.upImgArr_listen || [];
              let arr_listen = res.tempFiles;
              var temppath_imgArr_listen = t.data.path_upImgArr_listen || [];
              var i = 0;
              //console.log(1, temppath_imgArr)
              for (i in arr_listen) {
                temppath_imgArr_listen.push(arr_listen[i]['path'])
              }
              //console.log(res)
              //console.log(t)
              arr_listen.map(function (v, i) {
                wx.getFileSystemManager().readFile({
                  filePath: res.tempFilePaths[i], //选择图片返回的相对路径
                  encoding: 'base64', //编码格式
                  success: res => { //成功的回调
                    //console.log('data:image/png;base64,' + res.data)
                    v['base64'] = res.data;
                  }
                })
                v['progress'] = 0;
                imgArr_listen.push(v)
              })
              //console.log("啥情况",imgArr_listen)
              t.data.upImgArr_listen = imgArr_listen
              t.setData({
                path_upImgArr_listen: temppath_imgArr_listen
              })

              let upFilesArr_listen = getPathArr_ielts_listen(t);
              if (upFilesArr_listen.length > count - 1) {
                let imgArr_listen = t.data.upImgArr_listen;
                let newimgArr_listen = imgArr_listen.slice(0, count)
                t.setData({
                  upFilesBtn_listen: false,
                  upImgArr_listen: newimgArr_listen
                })
              }
            }
            if (uploadindex == 4) {
              var imgArr_speak = t.data.upImgArr_speak || [];
              let arr_speak = res.tempFiles;
              var temppath_imgArr_speak = t.data.path_upImgArr_speak || [];
              var i = 0;
              //console.log(1, temppath_imgArr)
              for (i in arr_speak) {
                temppath_imgArr_speak.push(arr_speak[i]['path'])
              }
              //console.log(res)
              //console.log(t)
              arr_speak.map(function (v, i) {
                wx.getFileSystemManager().readFile({
                  filePath: res.tempFilePaths[i], //选择图片返回的相对路径
                  encoding: 'base64', //编码格式
                  success: res => { //成功的回调
                    //console.log('data:image/png;base64,' + res.data)
                    v['base64'] = res.data;
                  }
                })
                v['progress'] = 0;
                imgArr_speak.push(v)
              })
              //console.log("查看你一下", imgArr_speak)
              t.data.upImgArr_speak =  imgArr_speak
              t.setData({         
                path_upImgArr_speak: temppath_imgArr_speak
              })

              let upFilesArr_speak = getPathArr_ielts_speak(t);
              if (upFilesArr_speak.length > count - 1) {
                let imgArr_speak = t.data.upImgArr_speak;
                let newimgArr_speak = imgArr_speak.slice(0, count)
                t.setData({
                  upFilesBtn_speak: false,
                  upImgArr_speak: newimgArr_speak
                })
              }
            }
            if (uploadindex == 5) {
              var imgArr_blank = t.data.upImgArr_blank || [];
              let arr_blank = res.tempFiles;
              var temppath_imgArr_blank = t.data.path_upImgArr_blank || [];
              var i = 0;
              //console.log(1, temppath_imgArr)
              for (i in arr_blank) {
                temppath_imgArr_blank.push(arr_blank[i]['path'])
              }
              //console.log(res)
              //console.log(t)
              arr_blank.map(function (v, i) {
                wx.getFileSystemManager().readFile({
                  filePath: res.tempFilePaths[i], //选择图片返回的相对路径
                  encoding: 'base64', //编码格式
                  success: res => { //成功的回调
                    //console.log('data:image/png;base64,' + res.data)
                    v['base64'] = res.data;
                  }
                })
                v['progress'] = 0;
                imgArr_blank.push(v)
              })
              //console.log("查看你一下", imgArr_blank)
              t.data.upImgArr_blank = imgArr_blank
              t.setData({
                path_upImgArr_blank: temppath_imgArr_blank
              })

              let upFilesArr_blank = getPathArr_toefl_blank(t);
              if (upFilesArr_blank.length > count - 1) {
                let imgArr_blank = t.data.upImgArr_blank;
                let newimgArr_blank = imgArr_blank.slice(0, count)
                t.setData({
                  upFilesBtn_blank: false,
                  upImgArr_blank: newimgArr_blank
                })
              }
            }
            if (uploadindex == 6) {
              var imgArr_math = t.data.upImgArr_math || [];
              let arr_math = res.tempFiles;
              var temppath_imgArr_math = t.data.path_upImgArr_math || [];
              var i = 0;
              //console.log(1, temppath_imgArr)
              for (i in arr_math) {
                temppath_imgArr_math.push(arr_math[i]['path'])
              }
              //console.log(res)
              //console.log(t)
              arr_math.map(function (v, i) {
                wx.getFileSystemManager().readFile({
                  filePath: res.tempFilePaths[i], //选择图片返回的相对路径
                  encoding: 'base64', //编码格式
                  success: res => { //成功的回调
                    //console.log('data:image/png;base64,' + res.data)
                    v['base64'] = res.data;
                  }
                })
                v['progress'] = 0;
                imgArr_math.push(v)
              })
              //console.log("查看你一下", imgArr_math)
              t.data.upImgArr_math = imgArr_math
              t.setData({
                path_upImgArr_math: temppath_imgArr_math
              })

              let upFilesArr_math = getPathArr_toefl_math(t);
              if (upFilesArr_math.length > count - 1) {
                let imgArr_math = t.data.upImgArr_math;
                let newimgArr_math = imgArr_math.slice(0, count)
                t.setData({
                  upFilesBtn_math: false,
                  upImgArr_math: newimgArr_math
                })
              }
            }
            if (uploadindex == 7) {
              var imgArr_logic = t.data.upImgArr_logic || [];
              let arr_logic = res.tempFiles;
              var temppath_imgArr_logic = t.data.path_upImgArr_logic || [];
              var i = 0;
              //console.log(1, temppath_imgArr)
              for (i in arr_logic) {
                temppath_imgArr_logic.push(arr_logic[i]['path'])
              }
              //console.log(res)
              //console.log(t)
              arr_logic.map(function (v, i) {
                wx.getFileSystemManager().readFile({
                  filePath: res.tempFilePaths[i], //选择图片返回的相对路径
                  encoding: 'base64', //编码格式
                  success: res => { //成功的回调
                    //console.log('data:image/png;base64,' + res.data)
                    v['base64'] = res.data;
                  }
                })
                v['progress'] = 0;
                imgArr_logic.push(v)
              })
              //console.log("查看你一下", imgArr_logic)
              t.data.upImgArr_logic = imgArr_logic
              t.setData({
                path_upImgArr_logic: temppath_imgArr_logic
              })

              let upFilesArr_logic = getPathArr_gmat_logic(t);
              if (upFilesArr_logic.length > count - 1) {
                let imgArr_logic = t.data.upImgArr_logic;
                let newimgArr_logic = imgArr_logic.slice(0, count)
                t.setData({
                  upFilesBtn_logic: false,
                  upImgArr_logic: newimgArr_logic
                })
              }
            }
            if (uploadindex == 8) {
              var imgArr_grammar = t.data.upImgArr_grammar || [];
              let arr_grammar = res.tempFiles;
              var temppath_imgArr_grammar = t.data.path_upImgArr_grammar || [];
              var i = 0;
              //console.log(1, temppath_imgArr)
              for (i in arr_grammar) {
                temppath_imgArr_grammar.push(arr_grammar[i]['path'])
              }
              //console.log(res)
              //console.log(t)
              arr_grammar.map(function (v, i) {
                wx.getFileSystemManager().readFile({
                  filePath: res.tempFilePaths[i], //选择图片返回的相对路径
                  encoding: 'base64', //编码格式
                  success: res => { //成功的回调
                    //console.log('data:image/png;base64,' + res.data)
                    v['base64'] = res.data;
                  }
                })
                v['progress'] = 0;
                imgArr_grammar.push(v)
              })
              //console.log("查看你一下", imgArr_grammar)
              t.data.upImgArr_grammar = imgArr_grammar
              t.setData({
                path_upImgArr_grammar: temppath_imgArr_grammar
              })

              let upFilesArr_grammar = getPathArr_gmat_grammar(t);
              if (upFilesArr_grammar.length > count - 1) {
                let imgArr_grammar = t.data.upImgArr_grammar;
                let newimgArr_grammar = imgArr_grammar.slice(0, count)
                t.setData({
                  upFilesBtn_grammar: false,
                  upImgArr_grammar: newimgArr_grammar
                })
              }
            }
          },
      });

  //console.log("上传后的信息", t.data)  
    
}

var chooseImageRead = (t, count) =>{
  wx.chooseImageRead({
    count: count,
    sizeType: ['original', 'compressed'],
    sourceType: ['album', 'camera'],
    /**success: (res) => {
      var imgArr = t.data.upImgArr || [];
      let arr = res.tempFiles;
      arr.map(function (v, i) {
        v['progress'] = 0;
        imgArr.push(v)
      })
      t.setData({
        upImgArr_read: imgArr
      })

    },**/
  });

}
var chooseVideo = (t,count) => {
    wx.chooseVideo({
        sourceType: ['album', 'camera'],
        maxDuration: 30,
        compressed:true,
        camera: 'back',
        success: function (res) {
            let videoArr = t.data.upVideoArr || [];
            let videoInfo = {};
            videoInfo['tempFilePath'] = res.tempFilePath;
            videoInfo['size'] = res.size;
            videoInfo['height'] = res.height;
            videoInfo['width'] = res.width;
            videoInfo['thumbTempFilePath'] = res.thumbTempFilePath;
            videoInfo['progress'] = 0;
            videoArr.push(videoInfo)
            t.setData({
                upVideoArr: videoArr
            })
            let upFilesArr = getPathArr(t);
            if (upFilesArr.length > count - 1) {
                t.setData({
                    upFilesBtn: false,
                })
            }
            // console.log(res)
        }
    })
}

// 获取 图片数组 和 视频数组 以及合并数组
var getPathArr = t => {
    let imgarr = t.data.upImgArr || [];
    let imgPathArr = [];
    imgarr.map(function (v, i) {
        imgPathArr.push(v.path)
    })
    let filesPathsArr = imgPathArr
    return filesPathsArr;
}

var getPathArr_ielts_read = t => {
  let imgarr_ielts_read = t.data.upImgArr_read || [];
  let imgPathArr_ielts_read = [];
  imgarr_ielts_read.map(function (v, i) {
    imgPathArr_ielts_read.push(v.path)
  })
  let filesPathsArr_ielts_read = imgPathArr_ielts_read
  return filesPathsArr_ielts_read;
}

var getPathArr_ielts_write = t => {
  let imgarr_ielts_write = t.data.upImgArr_write || [];
  let imgPathArr_ielts_write = [];
  imgarr_ielts_write.map(function (v, i) {
    imgPathArr_ielts_write.push(v.path)
  })
  let filesPathsArr_ielts_write = imgPathArr_ielts_write
  return filesPathsArr_ielts_write;
}

var getPathArr_ielts_speak = t => {
  let imgarr_ielts_speak = t.data.upImgArr_speak || [];
  let imgPathArr_ielts_speak = [];
  imgarr_ielts_speak.map(function (v, i) {
    imgPathArr_ielts_speak.push(v.path)
  })
  let filesPathsArr_ielts_speak = imgPathArr_ielts_speak
  return filesPathsArr_ielts_speak;
}

var getPathArr_ielts_listen = t => {
  let imgarr_ielts_listen = t.data.upImgArr_listen || [];
  let imgPathArr_ielts_listen = [];
  imgarr_ielts_listen.map(function (v, i) {
    imgPathArr_ielts_listen.push(v.path)
  })
  let filesPathsArr_ielts_listen = imgPathArr_ielts_listen
  return filesPathsArr_ielts_listen;
}

var getPathArr_toefl_math = t => {
  let imgarr_toefl_math = t.data.upImgArr_math || [];
  let imgPathArr_toefl_math = [];
  imgarr_toefl_math.map(function (v, i) {
    imgPathArr_toefl_math.push(v.path)
  })
  let filesPathsArr_toefl_math = imgPathArr_toefl_math
  return filesPathsArr_toefl_math;
}

var getPathArr_toefl_blank = t => {
  let imgarr_toefl_blank = t.data.upImgArr_blank || [];
  let imgPathArr_toefl_blank = [];
  imgarr_toefl_blank.map(function (v, i) {
    imgPathArr_toefl_blank.push(v.path)
  })
  let filesPathsArr_toefl_blank = imgPathArr_toefl_blank
  return filesPathsArr_toefl_blank;
}

var getPathArr_gmat_logic = t => {
  let imgarr_gmat_logic = t.data.upImgArr_logic || [];
  let imgPathArr_gmat_logic = [];
  imgarr_gmat_logic.map(function (v, i) {
    imgPathArr_gmat_logic.push(v.path)
  })
  let filesPathsArr_gmat_logic = imgPathArr_gmat_logic
  return filesPathsArr_gmat_logic;
}

var getPathArr_gmat_grammar = t => {
  let imgarr_gmat_grammar = t.data.upImgArr_grammar || [];
  let imgPathArr_gmat_grammar = [];
  imgarr_gmat_grammar.map(function (v, i) {
    imgPathArr_gmat_grammar.push(v.path)
  })
  let filesPathsArr_gmat_grammar = imgPathArr_gmat_grammar
  return filesPathsArr_gmat_grammar;
}
/**
 * upFilesFun(this,object)
 * object:{
 *    url     ************   上传路径 (必传)
 *    filesPathsArr  ******  文件路径数组
 *    name           ******  wx.uploadFile name
 *    formData     ******    其他上传的参数
 *    startIndex     ******  开始上传位置 0
 *    successNumber  ******     成功个数
 *    failNumber     ******     失败个数
 *    completeNumber  ******    完成个数
 * }
 * progress:上传进度
 * success：上传完成之后
 */

var upFilesFun = (t, data, progress, success) =>{
    let _this = t;
    let url = data.url;
    let filesPath = data.filesPathsArr ? data.filesPathsArr : getPathArr(t);
    let name = data.name || 'file';
    let formData = data.formData || {};
    let startIndex = data.startIndex ? data.startIndex : 0;
    let successNumber = data.successNumber ? data.successNumber : 0;
    let failNumber = data.failNumber ? data.failNumber : 0;
    if (filesPath.length == 0) {
      success([]);
      return;
    }
    const uploadTask = wx.uploadFile({
        url: url,
        filePath: filesPath[startIndex],
        name: name,
        formData: formData,
        success: function (res) {
            var data = res.data
            successNumber++;
            // console.log('success', successNumber)
            // console.log('success',res)
            // 把后台返回的地址链接存到一个数组
            let uploaded = t.data.uploadedPathArr || [];
            var da = JSON.parse(res.data);
            // console.log(da)
            if (da.code == 1001) {
                // ### 此处可能需要修改 以获取图片路径
                uploaded.push(da.data)

                t.setData({
                    uploadedPathArr: uploaded
                })
            }
        },
        fail: function(res){
            failNumber++;
            // console.log('fail', filesPath[startIndex])
            // console.log('failstartIndex',startIndex)
            // console.log('fail', failNumber)
            // console.log('fail', res)
        },
        complete: function(res){

            if (startIndex == filesPath.length - 1 ){
                // console.log('completeNumber', startIndex)
                // console.log('over',res)
                let sucPathArr = t.data.uploadedPathArr;
                success(sucPathArr);
                t.setData({
                    uploadedPathArr: []
                })
                //console.log('成功：' + successNumber + " 失败：" + failNumber)
            }else{
                startIndex++;
                // console.log(startIndex)
                data.startIndex = startIndex;
                data.successNumber = successNumber;
                data.failNumber = failNumber;
                upFilesFun(t, data, progress, success);
            }
        }
    })

    uploadTask.onProgressUpdate((res) => {
        res['index'] = startIndex;
        // console.log(typeof (progress));
        if (typeof (progress) == 'function') {
            progress(res);
        }
        // console.log('上传进度', res.progress)
        // console.log('已经上传的数据长度', res.totalBytesSent)
        // console.log('预期需要上传的数据总长度', res.totalBytesExpectedToSend)
    })

}
module.exports = { chooseImage, chooseVideo, upFilesFun, getPathArr}