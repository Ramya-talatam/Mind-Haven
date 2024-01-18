const msgerForm = get(".msger-inputarea");
    const msgerInput = get(".msger-input");
    const msgerChat = get(".msger-chat");
    var qno=1;
function typeWriter(txt,n)
{
  var i = 0;
var speed = 50;
function type() {
  if (i < txt.length) {
    document.getElementById("demo"+n.toString()).innerHTML += txt.charAt(i);
    i++;
    setTimeout(type, speed);
  }
}
type()
}
   
    // Icons made by Freepik from www.flaticon.com
    const BOT_IMG = "https://image.flaticon.com/icons/svg/327/327779.svg";
    const PERSON_IMG = "https://image.flaticon.com/icons/svg/145/145867.svg";
    const BOT_NAME = "    ChatBot";
    const PERSON_NAME = "You";
    const msgText = "Hi, welcome to ChatBot! Go ahead and send me a message. 😄";
    var n=1;
    appendMessage(BOT_NAME, BOT_IMG, "left",msgText,n);
    typeWriter(msgText,n);
    msgerForm.addEventListener("submit", event => {
      event.preventDefault();

      const msgText = msgerInput.value;
      if (!msgText) return;

      appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText,n);
      msgerChat.scrollTop = msgerChat.scrollHeight;
      msgerInput.value = "";
      submitAnswer(msgText);
    });

    function appendMessage(name, img, side, text,n) {
      //   Simple solution for small apps
      var txt=text
      if (side=='left') {
        txt="";
      }
      const msgHTML = `
<div class="msg ${side}-msg">
  <div class="msg-img" style="background-image: url(${img})"></div>

  <div class="msg-bubble">
    <div class="msg-info">
      <div class="msg-info-name">${name}</div>
      <div class="msg-info-time">${formatDate(new Date())}</div>
    </div>

    <div id="demo${n}" class="msg-text">${txt}</div>
  </div>
</div>
`;

      msgerChat.insertAdjacentHTML("beforeend", msgHTML);
      msgerChat.scrollTop = Math.min(500+msgerChat.scrollTop,msgerChat.scrollHeight) ;
    }
    function submitAnswer(answer) {
            $.ajax({
                url: '/record_answer',
                type: 'POST',
                data: {answer: answer,qno:qno},
                success: function(data) {
                  qno=data.qno;
                    botResponse();
                }
            });
        }
    function botResponse() {

           $.ajax({
                url: '/get_question',
                type: 'POST',
                data:{qno:qno},
                success: function(data) {
                    if (data.question === 'stop') {
                        var msg="Thank you for the conversation! type restart to restart the conversation";
                        
                    } else {
                        var msg=data.question;
                    }
                    n++;
        appendMessage(BOT_NAME, BOT_IMG, "left", msg,n);
        typeWriter(msg,n);
        msgerChat.scrollTop = msgerChat.scrollHeight;
                }
            });

    }


    function get(selector, root = document) {
      return root.querySelector(selector);
    }
    function formatDate(date) {
      const h = "0" + date.getHours();
      const m = "0" + date.getMinutes();

      return `${h.slice(-2)}:${m.slice(-2)}`;
    }

    $(document).ready(function() {
            botResponse();
        });
