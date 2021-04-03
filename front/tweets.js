/*
####################     tweets.js    ####################
*/

function getCookie(name) {
  return document.cookie.split(';').filter(function(item) {
    return item.indexOf(name) !== -1;  // 이 표현?
  })[0];
};




$(document).ready(function() {
  var accessToken = (getCookie('token') || '').split('=')[1];
  var paramArr = (window.location.search.split('?')[1] || '').split('&');  // Query String을 split하여 paramArr에 저장
    // user id가 query string으로 들어온다. (from login.html \)
  var userId = '';

  // window.alert(document.cookie)
    
  paramArr.forEach(function (param) {
    if (param.indexOf('userid') !== -1) {
      userId = param.split('=')[1];
    }
  })

  if (userId) {

    $('.userId')
      .append(userId);  // Ajax의 load 메소드 사용 고려해볼 것.
  }

  if (accessToken) {
    $.ajax({
      method: 'GET',
      url: 'https://runtweetsystem.run.goorm.io/timeline',
      crossDomain: true,
      headers: {
        'Authorization': accessToken
      }
    })
    .done(function(msg) {
      var timeline = msg.timeline;

      if (timeline) {
        timeline.forEach(function (item) {
          $('.timeline-container')
            .append('<div class="card">' +
              '<div class="card-body">' +
              '<h5 class="card-title">'+item.user_id+'</h5>' +
              '<p class="card-text">'+item.tweet+'</p></div>' +
              '</div>')
        })
      }
    });
  } else {
    alert('로그인이 필요합니다.');
    window.location.href = './login.html';
    return;
  }

  $('#tweetForm').submit(function(e) {
    e.preventDefault();  // 이 구문의 쓸모? 이것 때문에 tweet 엔드포인트에 중복 접속되는것인가?

    // if (!myId) {
    if (!accessToken) {
      alert('로그인이 필요합니다.');
      window.location.href = './login.html';
      return;
    }

    var tweet = $('#tweet').val();

    $.ajax({
      method: 'POST',
      url: 'https://runtweetsystem.run.goorm.io/tweet',
      headers: {
        'Authorization': accessToken
      },
      data: JSON.stringify({
        "id" : userId,  // 추가한 부분.
        "tweet" : tweet
      }),
      contentType: 'application/json'
    })
    .done(function(msg) {
      console.log(msg)
    });
  });

  $('#follow').on('click', function () {
    $.ajax({
      method: 'POST',
      url: 'https://runtweetsystem.run.goorm.io/follow',
      headers: {
        'Authorization': accessToken
      },
      data: JSON.stringify({
        "follow" : userId
      }),
      contentType: 'application/json'
    })
      .done(function(msg) {
        console.log(msg)
      });
  });

  $('#unfollow').on('click', function () {
    $.ajax({
      method: 'POST',
      url: 'https://runtweetsystem.run.goorm.io/unfollow',
      headers: {
        'Authorization': accessToken
      },
      data: JSON.stringify({
        "unfollow" : userId
      }),
      contentType: 'application/json'
    })
      .done(function(msg) {
        console.log(msg)
      });
  });
});
