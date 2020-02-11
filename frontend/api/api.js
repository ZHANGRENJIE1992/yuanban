let host = 'http://127.0.0.1:8001'

//let host = 'localhost'
// 用户注册url
var Registered = host + '/users/Registered/'

// 用户登录url
var login = host + '/users/login/'

// 获取用户个人信息和修改用户个人信息
var GetUser = host + '/users/GetUser/'

//提交ielts信息

var Ieltssubmitinfo = host + '/ielts/Create/'


module.exports = {
  login: login,
  GetUser: GetUser,
  Registered: Registered,
  Ieltssubmitinfo, Ieltssubmitinfo,
}