function createCookie(value) {
  var now = new Date();
  var expirationDate = new Date(now.getFullYear(), now.getMonth(), now.getDate()+7, 0, 0, 0);

  document.cookie = 'token='+value+'; expires='+expirationDate+'; path=/';
  /*
  document.cookie = 'token='+value;
  document.cookie = 'expires='+expirationDate;
  document.cookie = 'path=/';
  */
  
    // Cookie = 'token=something; expires=Date; path=/';
};

$(document).ready(function() {
  $("#loginForm").submit(function(e) {
    e.preventDefault();

    var id = $("#id").val();  // form에서 입력된 email
    var password = $("#password").val();  // form에서 입력된 password

    $.ajax({
      method: "POST",
      url: "https://runtweetsystem.run.goorm.io/login",
      data: JSON.stringify({
        "email"    : id,
        "password" : password  // JSON payload
      }),
      contentType: 'application/json'
    })
    .done(function(msg) {  // msg는 어떤 parameter인가?
        // HTTP 요청이 성공하면 요청한 데이터가 done() method로 전달된다.
        // tweetsystem의 /login 엔드포인트의 return값은 jsonify({'access_token': access_token})이다.
        // 즉, msg가 이 JSON 데이터.
      if (msg.access_token) {
        createCookie(msg.access_token);  // /login 엔드포인트에서 받아온 access_token으로 createCookie.
        // window.alert(document.cookie);
        window.location.href = './tweets.html?userid='+msg.user_id;
      }
    });
  });
});
