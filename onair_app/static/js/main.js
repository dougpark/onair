// https://flask-socketio.readthedocs.io/en/latest/intro.html

var socket = io()

function init() {
    var loggerElement = document.getElementById('logger')
    var dataElement = document.createElement('pre')
    loggerElement.innerHTML = ''
    dataElement.innerHTML = "Server Started"
    loggerElement.appendChild(dataElement)

    console.log('sending first connect/one to server:')
    socket.emit('one', {data: 'connect/one'})

    console.log('sending mirror/one to server:')
    socket.emit('mirror', {data: 'First mirror data sent from client'})

    console.log('sending mirror/two to server:')
    socket.emit('mirror', {data: 'Second mirror data sent from client'})

    socket.on('mirrorResp', function (payload) {
        console.log('mirror response from server:')
        console.log(payload)
        var dataElement = document.createElement('pre')
        dataElement.innerHTML = payload.data
        loggerElement.appendChild(dataElement)
    })

    socket.on('oneResp', function (payload) {
        console.log('one response from server:')
        console.log(payload)
        var dataElement = document.createElement('pre')
        dataElement.innerHTML = payload.data
        loggerElement.appendChild(dataElement)
    })

    socket.on('connectResp', function (payload) {
        console.log('connect response from server:')
        console.log(payload)
        var dataElement = document.createElement('pre')
        dataElement.innerHTML = payload.data
        loggerElement.appendChild(dataElement)
    })
  
    

}

function initRefresh() {
  $("#refresh").click(function (e) {
    var idClicked = e.target.id;
    console.log(idClicked)
  
    refresh()
  
  });

  function refresh() {
    console.log('sending refresh to server:')
    socket.emit('refresh', {data: 'Refresh sent from client'})
  }

  socket.on('refreshResp', function (payload) {
    console.log('refresh response from server:')
    console.log(payload)
    // var loggerElement = document.getElementById('logger')
    var dataElement = document.getElementById('refreshVal')
    // dataElement.innerHTML = payload.data
    // loggerElement.appendChild(dataElement)
  })

}

function initMessage() {
  $("#showMsg").click(function (e) {
    var idClicked = e.target.id;
    console.log(idClicked)
    showMsg()
  });

  function showMsg() {
    console.log('sending showMsg to server:')
    socket.emit('showmsg', {data: 'showMsg sent from client'})
  }

  $("#hideMsg").click(function (e) {
    var idClicked = e.target.id;
    console.log(idClicked)
    hideMsg()
  });

  function hideMsg() {
    console.log('sending hideMsg to server:')
    socket.emit('hidemsg', {data: 'hideMsg sent from client'})
  }

  socket.on('update', function (payload) {
    console.log('update response from server:')
    console.log(payload)
    // var loggerElement = document.getElementById('logger')
    var dataElement = document.getElementById('displayMsg')
    var dataElementC = document.getElementById('displayMsgC')
    var dataElementT = document.getElementById('sessionTime')
    var dataElementR = document.getElementById('sessionRemaining')

    if (payload.adminPanel == true) {
      document.getElementById("adminPanel").style.display = "block";
    }

    if (payload.onAir == true) {
      dataElement.innerHTML = payload.sessionMessage
      dataElementT.innerHTML = payload.sessionNow
      dataElementR.innerHTML = payload.sessionRemaining
      dataElement.classList.add("w3-red")
      dataElement.classList.remove("w3-green")
      dataElement.classList.remove("w3-black")
      dataElementC.classList.add("w3-red")
      dataElementC.classList.remove("w3-green")
    } else {
      dataElement.innerHTML = 'Ready'
      dataElement.classList.add("w3-green")
      dataElement.classList.remove("w3-red")
      dataElement.classList.remove("w3-black")
      dataElementC.classList.add("w3-green")
      dataElementC.classList.remove("w3-red")
    }
    // loggerElement.appendChild(dataElement)
  })

  // socket.emit('getrefresh', {data: 'getRefresh sent from client'})
  socket.emit('getstatus', {data: 'getStatus sent from client'})
}



function openTab(evt, tabName) {
  var i, tabs, tablinks;
  tabs = document.getElementsByClassName("tab");
  for (i = 0; i < tabs.length; i++) {
      tabs[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" w3-border-red", " w3-border-blue");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " w3-border-red";
}


$(window).on("load", function () {
  // init()
  initRefresh()
  initMessage()
  console.log('init completed')
})
