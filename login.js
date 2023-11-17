// login.js
document.addEventListener("DOMContentLoaded", function () {
  const loginButton = document.getElementById("login-button");

  loginButton.addEventListener("click", function () {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // 여기서 로그인 검증 로직을 수행합니다. (예: 서버로 요청하여 검증)

    // 로그인이 성공하면 다른 페이지로 이동합니다.
    if (username === "testID" && password === "testPASSWORD") {
      window.location.href = "main.html"; // 다른 페이지로 이동
    } else {
      alert("로그인 실패. 사용자 이름과 비밀번호를 다시 확인하세요.");
    }
  });
});
