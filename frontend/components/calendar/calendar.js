// components/calendar/calendar.js
/**
 * 日历选择组件
 * 2018-03-04
 * mehaotian
 * github ：https://github.com/mehaotian
 */
var Request = require("../../utils/request.js");
var Api = require("../../api/api.js")

Component({
  /**
   * 组件的属性列表
   * data [Date] 当前现实的月份
   * selected [Array] 所有被选择的天
   */
  properties: {
    date: {
      type: null,
      value: new Date()
    },
    selected: {
      type: Array,
      value: [],
      observer(newVal, oldVal) {
        this.getWeek(new Date())
      }
    },
    isOpen: {
      type: Boolean,
      value: false,
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
    calShow: true, // 日历组件是否打开
    dateShow: false, // 日期是否选择
    selectDay: '', // 当前选择日期
    canlender: {
      "weeks": []
    },
    ielts:[1,2,3],
    toefl:[],
    gre:[],
    gmat:[]
  },


  ready() {
    this.getWeek(new Date())
    if (this.data.isOpen) {
      this.setData({
        calShow: false,
        dateShow: true
      })
    }
  },
  /**
   * 组件的方法列表
   */
  methods: {
    dateSelection() {
      if (this.data.isOpen) {
        return
      }
      let self = this;
      if (self.data.calShow) {
        self.setData({
          calShow: false
        }, () => {
          setTimeout(() => {
            self.setData({
              dateShow: true
            }, () => {
              self.triggerEvent('select', { ischeck: !self.data.calShow })
            })
          }, 100)
        })
      } else {
        self.setData({
          dateShow: false
        }, () => {
          setTimeout(() => {
            self.setData({
              calShow: true
            }, () => {
              self.triggerEvent('select', { ischeck: !self.data.calShow })
            })
          }, 300)
        })
      }

    },
    selectDay(e) {

      let index = e.currentTarget.dataset.index;
      console.log("index", index)
      let week = e.currentTarget.dataset.week;
      let ischeck = e.currentTarget.dataset.ischeck;
      let canlender = this.data.canlender;
      if (!ischeck) return false;
      let month = canlender.weeks[week][index].month < 10 ? "0" + canlender.weeks[week][index].month : canlender.weeks[week][index].month
      let date = canlender.weeks[week][index].date < 10 ? "0" + canlender.weeks[week][index].date : canlender.weeks[week][index].date
      this.getWeek(canlender.year + "-" + month + "-" + date);

    },
    packup() {

      let self = this;
      if (this.data.isOpen) {
        let year = self.data.canlender.year + "-" + self.data.canlender.month + "-" + self.data.canlender.date
        let _date = self.getDate(year, 0);
        self.getWeek(_date);
        return
      }
      self.setData({
        dateShow: false
      }, () => {
        setTimeout(() => {
          self.setData({
            calShow: true
          }, () => {
            let year = self.data.canlender.year + "-" + self.data.canlender.month + "-" + self.data.canlender.date
            let _date = self.getDate(year, 0);
            self.getWeek(_date);
            self.triggerEvent('select', { ischeck: !self.data.calShow })
          })
        }, 300)
      })
    },
    // 返回今天
    backtoday() { this.getWeek(new Date()); },
    // 前一天|| 后一天
    dataBefor(e) {
      let num = 0;
      let types = e.currentTarget.dataset.type;

      if (e.currentTarget.dataset.id === "0") {
        num = -1;
      } else {
        num = 1
      }
      let year = this.data.canlender.year + "-" + this.data.canlender.month + "-" + this.data.canlender.date
      let _date = this.getDate(year, num, types === 'month' ? "month" : "day");
      this.getWeek(_date);
    },
    // 获取日历内容
    getWeek(dateData) {
      var _this = this
      let selected = this.data.selected
      let a = new Date()
      // console.log("im date ", a, typeof a === 'object')
      // 判断当前是 安卓还是ios ，传入不容的日期格式
      //console.log("dateData", dateData)
      if (typeof dateData !== 'object') {
        dateData = dateData.replace(/-/g, "/")
      }
      let _date = new Date(dateData);
      let year = _date.getFullYear(); //年
      let month = _date.getMonth() + 1;  //月
      let date = _date.getDate();//日
      let day = _date.getDay();// 天
      let canlender = [];
      let yearmonth = year+"-"+month;
      let ielts = this.data.ielts;
      let toefl = this.data.toefl;
      let gre = this.data.gre;
      let gmat = this.data.gmat;
      let sign = 0;
      console.log("riqi:", yearmonth)
      // console.log(selected)
      let dates = {
        firstDay: new Date(year, month - 1, 1).getDay(),
        lastMonthDays: [],// 上个月末尾几天
        currentMonthDys: [], // 本月天数
        nextMonthDays: [], // 下个月开始几天
        endDay: new Date(year, month, 0).getDay(),
        weeks: []
      }
      Request.request(Api.Ieltslist, { month: yearmonth }, 'GET').then(function (res) {
        let ieltsData = res.data.data
        Request.request(Api.Toefllist, { month: yearmonth }, 'GET').then(function (res) {   
          let toeflData = res.data.data
          Request.request(Api.Grelist, { month: yearmonth }, 'GET').then(function (res) {
           let greData = res.data.data
            Request.request(Api.Gmatlist, { month: yearmonth }, 'GET').then(function (res) {
              let gmatData = res.data.data
              console.log("gmat", gmat)
              // 循环上个月末尾几天添加到数组
              for (let i = dates.firstDay; i > 0; i--) {
                dates.lastMonthDays.push({
                  'date': new Date(year, month, -i).getDate() + '',
                  'month': month - 1
                })
              }

              // 循环本月天数添加到数组
              for (let i = 1; i <= new Date(year, month, 0).getDate(); i++) {
                let have = false;
                for (let j = 0; j < selected.length; j++) {
                  let selDate = selected[j].date.split('-');

                  if (Number(year) === Number(selDate[0]) && Number(month) === Number(selDate[1]) && Number(i) === Number(selDate[2])) {
                    have = true;
                  }
                  }
                console.log("chakan", ieltsData[i - 1])
                if (ieltsData[i - 1].sign == 2 || toeflData[i - 1].sign == 2 || greData[i - 1].sign == 2 || gmatData[i - 1].sign == 2) {
                  sign = 2
                } else if (ieltsData[i - 1].sign == 1 || toeflData[i - 1].sign == 1 || greData[i - 1].sign == 1 || gmatData[i - 1].sign == 1) {
                  sign = 1
                } else {
                  sign = 0
                  
                }

                dates.currentMonthDys.push({
                  'date': i + "",
                  'month': month,
                  have,
                  sign
                })
              }
              // 循环下个月开始几天 添加到数组
              for (let i = 1; i < 7 - dates.endDay; i++) {
                dates.nextMonthDays.push({
                  'date': i + '',
                  'month': month + 1
                })
              }

              canlender = canlender.concat(dates.lastMonthDays, dates.currentMonthDys, dates.nextMonthDays)
              // 拼接数组  上个月开始几天 + 本月天数+ 下个月开始几天
              for (let i = 0; i < canlender.length; i++) {
                if (i % 7 == 0) {
                  dates.weeks[parseInt(i / 7)] = new Array(7);
                }
                dates.weeks[parseInt(i / 7)][i % 7] = canlender[i]
              }


              // 渲染数据
              console.log("dates.weeks", dates.weeks)
              console.log("month", month)
              console.log("date", date)
              _this.setData({//关注
                selectDay: month + "月" + date + "日",
                "canlender.weeks": dates.weeks,
                'canlender.month': month,
                'canlender.date': date,
                "canlender.day": day,
                'canlender.year': year,
              })
              month = month < 10 ? "0" + month : month
              date = date < 10 ? "0" + date : date
              _this.triggerEvent('getdate', { year, month, date })//关注
            })
          })

        })
      
      })

    },
    /**
     * 时间计算
     */
    getDate(date, AddDayCount, str = 'day') {
      if (typeof date !== 'object') {
        date = date.replace(/-/g, "/")
      }
      let dd = new Date(date)
      switch (str) {
        case 'day':
          dd.setDate(dd.getDate() + AddDayCount)// 获取AddDayCount天后的日期
          break;
        case 'month':
          dd.setMonth(dd.getMonth() + AddDayCount)// 获取AddDayCount天后的日期
          break;
        case 'year':
          dd.setFullYear(dd.getFullYear() + AddDayCount)// 获取AddDayCount天后的日期
          break;
      }
      let y = dd.getFullYear()
      let m = (dd.getMonth() + 1) < 10 ? '0' + (dd.getMonth() + 1) : (dd.getMonth() + 1)// 获取当前月份的日期，不足10补0
      let d = dd.getDate() < 10 ? '0' + dd.getDate() : dd.getDate()// 获取当前几号，不足10补0
      return y + '-' + m + '-' + d
    },

 
  }
})
