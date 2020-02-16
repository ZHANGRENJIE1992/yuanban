//let host = 'http://127.0.0.1:8001'
let host = 'https://yuanban.info'
//let host = 'localhost'、
// 用户注册url
var Registered = host + '/users/Registered/'

// 用户登录url
var login = host + '/users/login/'

// 获取用户个人信息和修改用户个人信息
var GetUser = host + '/users/GetUser/'

//提交ielts信息

var Ieltssubmitinfo = host + '/course/ielts/Create/'

var Ieltsgetinfo = host + '/course/GetIelts/'

//提交toefl信息
var Toeflsubmitinfo = host + '/course/toefl/Create/'

var Toeflgetinfo = host + '/course/GetToefl/'

//提交gre信息
var Gresubmitinfo = host +'/course/gre/Create/'

var Gregetinfo = host +'/course/GetGre'

//提交gmat信息
var Gmatsubmitinfo = host + '/course/gmat/Create/'

var Gmatgetinfo = host + '/course/GetGmat'

module.exports = {
  login: login,
  GetUser: GetUser,
  Registered: Registered,
  Ieltssubmitinfo: Ieltssubmitinfo,
  Ieltsgetinfo: Ieltsgetinfo,
  Toeflsubmitinfo: Toeflsubmitinfo,
  Toeflgetinfo: Toeflgetinfo,
  Gresubmitinfo: Gresubmitinfo,
  Gregetinfo: Gregetinfo,
  Gmatsubmitinfo: Gmatsubmitinfo,
  Gmatgetinfo: Gmatgetinfo,
}