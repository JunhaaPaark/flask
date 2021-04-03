$(document).ready(function() {
  $("#signupForm").submit(function(e) {
    e.preventDefault();  // 특정 이벤트 중단

    var email    = $("#email").val();
    var name     = $("#name").val();
    var password = $("#password").val();

      
    $.ajax({
      method: "POST",
      url: "https://runtweetsystem.run.goorm.io/sign-up",
      data: JSON.stringify({
        "email"    : email,
        "name"     : name,
        "password" : password
      }),
      contentType: 'application/json'
    })
      .done(function(){
        window.location.href='/login.html';
    })

      
    /*  
    .done(function(msg) {
        console.log(msg)    
        window.location.href='/login.html';  // CORS 문제 해결 후 재시도할 것.
        */
        /*
        if (msg.email === email) {
          window.location.href = '/login.html';
            
       }  */ // CORS 정책 위반으로 인해 console log 오류
  });
});
