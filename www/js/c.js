// import ceshi from "../vues/ceshi.vue";

var  u = localStorage.getItem('username')  // 全局


var socket = null;
var vue = new Vue({
    el: "#app",
    data: {
        ClassFlag: 1,
        text: '',
        bt_status: 0,
        area_status: false,
        chatMessage: [{name: '小明', tiwen: '请用python写一个for循环', daan: '好的下面是...'},],
        loginFlag: false,
        registerFlag: false,
        community_input: '',
        prims_ai: '',
        pwd: '',
        pwd2: '',
        email: '',
        username: u, // 用户名
        is_account: false,  // 登录状态
        on_line: 0,   // 在线人数
    },

    methods:  {
        // 定位到输入框
        t: function (){
            const t = this.$refs.textarea;
            console.log(t)
            alert("测试")
            t.scrollIntoView();
        },
        // gpt
        c: function () {
            socket = io.connect('ws://127.0.0.1:8000');
            // 测试
            socket.on('connect', (data) =>{
                this.on_line = data.number
                console.log("连接成功"+data.number)
            })
            socket.on('disconnect', (data)=>{
                this.on_line = data.number
                // 发送断开的用户
                socket.close()
            })
            // 我方
            socket.on('me', (data)=>{
                console.log("me:"+data)
                var html = "<article class=\"media\" style=\"padding: 20px 32px 10px 32px\">\n" +
                    "           <figure class=\"media-left\">\n" +
                    "           <p class=\"image is-32x32\">\n" +
                    "           <img src=\"https://bulma.io/images/placeholders/128x128.png\">\n" +
                    "           </figure>\n" +
                    "           <div class=\"media-content\">\n" +
                    "           <div class=\"content\">\n" +
                    "           <strong>生</strong> <small>@johnsmith</small> <small>31m</small>\n" +
                    "           <br>\n" +
                    "               <div>"+ data+ "</div>\n" +
                    "           </div>\n" +
                    "           </div>\n" +
                    "           </article>"
                $("#msgDiv").append(html+'<br>')

            })
            // ai
            socket.on('ai', (data)=>{
                var html = " <article class=\"media\" style=\"padding: 20px 32px 10px 32px; background-color: rgba(238,238,238,0.27); \" ><figure class=\"media-left\"><p class=\"image is-32x32\"> <img src=\"https://bulma.io/images/placeholders/128x128.png\"> </figure> <div class=\"media-content\"> <div class=\"content\"> <strong>虚无</strong> <small>2023-01-01</small> <small>31m</small> <br> <div class=\'dazi'\></div> </div> <nav class=\"level is-mobile\"> <div class=\"level-left\"> <a class=\"level-item\"> <span class=\"icon is-small\"><i class=\"fas fa-reply\"></i></span> </a> <a class=\"level-item\"> <span class=\"icon is-small\"><i class=\"fas fa-heart\"></i></span> </a> </div> </nav> </div> </article>\n"

                $("#msgDiv").append(html+'<br>')  // 先插入样式
                // mark格式化
                const converter = new showdown.Converter();
                const htmlText = converter.makeHtml(data);
                // 插入html。隐藏
                var o = $(".dazi:last")
                o.hide()  // 隐藏标签
                o.html(htmlText);  // 插入html
                // this.a()   // 调用高亮和打字机
                this.a()
                this.bt_status = 0
                this.area_status = false
                Prism.highlightAll();

            })
            // 社区
            socket.on('communitys', (data)=>{
                console.log("社区"+data.data)
                var username = data.username
                // 判断是否为本人
                if (username !== '游客') {
                    var html = "<article class=\"media\" ><figure class=\"media-left\" ><p class=\"image is-32x32 \"><img src=\"https://bulma.io/images/placeholders/128x128.png\" class=\"\"></p></figure><div class=\"media-content\"><div class=\"content\"><div><strong class=\"tag is-primary\">"+username+"</strong><br><div style=\"margin-top: 2px;background-color: #ebebeb;padding: 10px;border-radius: 5px;display: inline-block;\">"+data.message+"</div></div></div></div></article>\n"
                    $("#c_msg").append(html)
                } else {
                    var html = "<article class=\"media\" ><figure class=\"media-left\" ><p class=\"image is-32x32 \"><img src=\"https://bulma.io/images/placeholders/128x128.png\" class=\"\"></p></figure><div class=\"media-content\"><div class=\"content\"><div><strong class=\"tag is-dark\">"+username+"</strong><br><div style=\"margin-top: 2px;background-color: #ebebeb;padding: 10px;border-radius: 5px;display: inline-block;\">"+data.message+"</div></div></div></div></article>\n"
                    $("#c_msg").append(html)
                }
            })
        },

        // // 打字效果
        printText: function (text, object) {
          object.show();
          var i = 0;
          var html = '';
          var print = function() {
            html += text[i];
            object.html(html);
            i++;
            if (i < text.length) {
              requestAnimationFrame(print);
            }
          };

          requestAnimationFrame(print);

        },

        a: function(){
            // 时间太快，会自动识别代码失败
            setTimeout(this.b, 500)
            // this.bt_status = 0
            // this.area_status = false

        },
        // 获取高亮代码
        b: function () {
            var o = $(".dazi:last")
            this.prims_ai = o.html()  // 赋值
            this.printText(o.html(), o)  // 调用打字机
        },
        // 社区
        sendMsgCommunity: function (){
            if (this.ClassFlag === 3) {
                var token = sessionStorage.getItem('token')
                socket.emit('community', {'msg':this.community_input,'token':token})
                console.log("社区发送成功")
                this.community_input = ''
            }
        },
        // 发送
        send_message: function() {
            if (this.ClassFlag === 1) {
                var token = sessionStorage.getItem('token')
                socket.emit('msg', {'msg':this.text, 'token': token})
                this.text = ''
                this.bt_status = 1
                this.area_status = true
            }
        },
        // 房间数据
        get_message: function () {
            console.log("p")
            axios.post('http://127.0.0.1:8000/api')
                .then(response => {
                    console.log(response.data)
                    this.chatMessage = response.data
                    this.ClassFlag = 1
                })
        },
        // 注册
        register: function () {
            axios.post('http://127.0.0.1:8000/register', {'email': this.email, 'pwd': this.pwd, 'pwd2': this.pwd2})
                .then(response =>{
                    console.log(response.data)
                })
        },
        // 登录令牌
        setToken: function () {
            axios.post('http://127.0.0.1:8000/login', {'email': this.email, 'pwd': this.pwd})
                .then(response => {
                    // 设置token
                    // localStorage.token = response.data.token
                    sessionStorage.token = response.data.token
                    // 设置用户名
                    localStorage.username = response.data.username
                    console.log("获取的token:"+response.data.token)
                    if (localStorage.getItem('username') !== 'undefined') {
                        this.loginFlag = false  // 关闭登录窗口
                        this.is_account = true  // 显示登录状态
                        this.username = response.data.username
                    }
                })
        },
        // 退出登录
        delToken: function () {
            sessionStorage.clear()
            localStorage.clear()
            window.location.reload()

        }
    },
    created(){
        // 页面加载就触发
        this.c()
        // 判断登录状态
        if (u !== 'undefined' && u !== null) {
            this.is_account = true
        }else {
            u == null
        }
    },


})
