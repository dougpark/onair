// https://flask-socketio.readthedocs.io/en/latest/intro.html

var socket = io();

// not used
function init() {
  var loggerElement = document.getElementById("logger");
  var dataElement = document.createElement("pre");
  loggerElement.innerHTML = "";
  dataElement.innerHTML = "Server Started";
  loggerElement.appendChild(dataElement);

  //console.log('sending first connect/one to server:')
  socket.emit("one", { data: "connect/one" });

  //console.log('sending mirror/one to server:')
  socket.emit("mirror", { data: "First mirror data sent from client" });

  //console.log('sending mirror/two to server:')
  socket.emit("mirror", { data: "Second mirror data sent from client" });

  socket.on("mirrorResp", function (payload) {
    //console.log('mirror response from server:')
    //console.log(payload)
    var dataElement = document.createElement("pre");
    dataElement.innerHTML = payload.data;
    loggerElement.appendChild(dataElement);
  });

  socket.on("oneResp", function (payload) {
    //console.log('one response from server:')
    //console.log(payload)
    var dataElement = document.createElement("pre");
    dataElement.innerHTML = payload.data;
    loggerElement.appendChild(dataElement);
  });

  socket.on("connectResp", function (payload) {
    //console.log('connect response from server:')
    //console.log(payload)
    var dataElement = document.createElement("pre");
    dataElement.innerHTML = payload.data;
    loggerElement.appendChild(dataElement);
  });
}

// not used
function initRefresh() {
  $("#refresh").click(function (e) {
    var idClicked = e.target.id;
    //console.log(idClicked)

    refresh();
  });

  function refresh() {
    //console.log('sending refresh to server:')
    socket.emit("refresh", { data: "Refresh sent from client" });
  }

  socket.on("refreshResp", function (payload) {
    //console.log('refresh response from server:')
    //console.log(payload)
    // var loggerElement = document.getElementById('logger')
    var dataElement = document.getElementById("refreshVal");
    // dataElement.innerHTML = payload.data
    // loggerElement.appendChild(dataElement)
  });
}

// init on air messaging
function initMessage() {

  // handle start button
  $("#startSession").click(function (e) {
    var idClicked = e.target.id;
    //console.log(idClicked)
    startSession();
  });

  function startSession() {
    //console.log('sending startSession to server:')
    socket.emit("startSession", { data: "startSession sent from client" });
  }

  // handle stop button
  $("#stopSession").click(function (e) {
    var idClicked = e.target.id;
    //console.log(idClicked)
    stopSession();
  });

  function stopSession() {
    //console.log('sending stopSession to server:')
    socket.emit("stopSession", { data: "stopSession sent from client" });
  }

  // handle response from server
  socket.on("update", function (payload) {
    //console.log('update response from server:')
    console.log(payload);
    // var loggerElement = document.getElementById('logger')
    var dataElement = document.getElementById("displayMsg");
    var dataElementT = document.getElementById("sessionTime");
    var dataElementR = document.getElementById("sessionRemaining");

    var onair =
      `<span class="material-symbols-outlined">mic</span>` +
      " " +
      payload.sessionMessage;
    var offair =
      `<span class="material-symbols-outlined">mic_off</span>` +
      " " +
      payload.standByMessage;

    // show admin card if notified from server
    if (payload.adminPanel == true) {
      document.getElementById("adminPanel").style.display = "block";
    }

    // if settings card not displayed then update from server
    if (document.getElementById("settings").style.display == "none") {
      $("#saveDuration").val(payload.sessionDuration);
      $("#saveOnAirMessage").val(payload.sessionMessage);
      $("#saveStandByMessage").val(payload.standByMessage);
    }

    // process payload data from server
    if (payload.onAir == true) {
      dataElement.innerHTML = onair;
      dataElementT.innerHTML = payload.sessionNow;
      dataElementR.innerHTML = payload.sessionRemaining;
      $(".displayMsgC")
        .addClass("w3-red")
        .removeClass("dnp-dark-grey w3-black");
    } else {
      dataElement.innerHTML = offair;
      dataElementT.innerHTML = payload.sessionNow;
      dataElementR.innerHTML = "";
      $(".displayMsgC")
        .addClass("dnp-dark-grey")
        .removeClass("w3-red w3-black");
    }
  });

  // handle save setting button
  $("#saveSettingsBtn").click(function (e) {
    var idClicked = e.target.id;

    // close settings card
    document.getElementById("settings").style.display = "none";

    // validate duration to be a valid number
    var duration = $("#saveDuration").val()
    var newDuration = 0;
    if (isNaN(duration) || duration < 0 || duration > 1440) {
      newDuration = ""
    } else {
      newDuration = duration
    }

    // save to server
    var data = {};
    data.message = $("#saveOnAirMessage").val();
    data.standby = $("#saveStandByMessage").val();
    data.duration = newDuration;
    socket.emit("savesettings", data);
  });

  // on startup get the status
  socket.emit("getstatus", { data: "getStatus sent from client" });
}

// utility function to hide/show tabs in UI
function openTab(evt, tabName) {
  var i, tabs, tablinks;
  tabs = document.getElementsByClassName("tab");
  for (i = 0; i < tabs.length; i++) {
    tabs[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(
      " w3-border-red",
      " w3-border-blue"
    );
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " w3-border-red";
}

// utility fuction to hide/show named card
function toggleCard(cardName) {
  if (document.getElementById(cardName).style.display == "none")
    document.getElementById(cardName).style.display = "block";
  else document.getElementById(cardName).style.display = "none";
}

// init everything once the webpage has finished loading
$(window).on("load", function () {
  // init()
  // initRefresh();
  initMessage();
});
