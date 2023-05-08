var numOfKeywords = 10; // Number of keywords to be displayed on the popup
var url_curr = "";
var keywordArray = [];

var s = document.getElementsByClassName("selection");
var l = document.getElementById("loaderContainer");
var lt = document.getElementById("loaderText");
var c = document.getElementById("confirm");

// Request keyword extraction from the server as soon as the popup is opened
document.addEventListener("DOMContentLoaded", function () {
      chrome.runtime.sendMessage({
        "message": "getKeywords"
      }, function (response) {
        console.log("Keywords received from the server: " + response.keywords);
        keywordArray = response.keywords;
        for (var i = 0; i < numOfKeywords; i++) {
          var li = document.createElement("li");
          var t = document.createTextNode(keywordArray[i]);
          li.appendChild(t);
          document.getElementById("myUL").appendChild(li);
        }
        l.style.display = "none";
        s[0].style.display = "block";
      });
  });

var selected = [];

c.onclick = function (e) {
  var options = document.getElementsByClassName("checked");
  for (var i = 0; i < options.length; i++) {
    selected.push(options[i].firstChild.nodeValue);
  }

  chrome.runtime.sendMessage({
    "message": "searchInfo",
    "selected": selected
  });
  window.close();
}

// Create a "close" button and append it to each list item
var myNodelist = document.getElementsByTagName("LI");
var i;
for (i = 10; i < myNodelist.length; i++) {
  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  myNodelist[i].appendChild(span);
}

// Click on a close button to hide the current list item
var close = document.getElementsByClassName("close");
var i;
for (i = 0; i < close.length; i++) {
  close[i].onclick = function () {
    var div = this.parentElement;
    div.style.display = "none";
  }
}

// Add a "checked" symbol when clicking on a list item
var list = document.querySelector('ul');
list.addEventListener('click', function (ev) {
  if (ev.target.tagName === 'LI') {
    ev.target.classList.toggle('checked');
  }
}, false);

document.getElementById("addBtn").addEventListener("click", function () {
  var li = document.createElement("li");
  var inputValue = document.getElementById("myInput").value;
  var t = document.createTextNode(inputValue);
  li.appendChild(t);
  if (inputValue !== '') {
    document.getElementById("myUL").appendChild(li);
  }
  document.getElementById("myInput").value = "";

  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  li.appendChild(span);

  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      var div = this.parentElement;
      div.style.display = "none";
      if(keywordArray.indexOf(div.innerText) > -1) {
        keywordArray.splice(keywordArray.indexOf(div.innerText), 1);
      }
    }
  }
});