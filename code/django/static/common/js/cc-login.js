
  // bind listeners for buttons      
  $(document).on('click', '#login-button', function() { handleLogin(); });
  $(document).on('click', '#logout-button', function() { handleLogout(); });
  $(document).on('click', '#register-button', function() { handleRegister(); });
  $(document).on('click', '#change-button', function() { handlePwChange(); });

  $(document).on('click', '.auth-toggle', function(e) { handleAuthToggle(e); });

  async function handleLogin() {

    let username = $('#input_user').val();
    let password = $('#input_password').val();
    let remember = $('#input_remember').is(":checked");

    postData = { 'username': username, 'password': password, 'remember': remember };
    let result = await sendPost('/api/users/login/', postData);
    if (fetchFromObject(result, 'message') == 'login success') {
      if (nextUrl == '') { nextUrl = '/map/'; }
      window.location.href = nextUrl;
    }
    else {
      $('#auth-msg').html(result.message);
    }
  }

  async function handleLogout() {

    let result = await sendPost('/api/users/logout/', null);
    window.location.href = '/';
  }

  async function handleRegister() {

    let name = $('#input_name').val();
    let email = $('#input_email').val();
    let password = $('#input_password').val();
    let password_2 = $('#input_password_2').val();

    postData = { 'name': name, 'email': email, 'password': password, 'password_2': password_2 };
    let result = await sendPost('/api/users/register/', postData);
    console.log(result);
    $('#auth-msg').html(result.message);
    if (result.message == 'registration success') {
      setTimeout(function () {
        window.location.href = '/login/';
      }, 2500);
    }
  }

  async function handlePwChange() {

    let password = $('#input_password').val();
    let password_2 = $('#input_password_2').val();

    postData = { 'password': password, 'password_2': password_2 };
    let result = await sendPost('/update', postData);
    console.log(result);
    $('#auth-msg').html(result.message);
  }

  function handleAuthToggle(e) {

    let link = e.target.id;
    let elem = '#auth-container';

    if (link == 'login-link') { renderLogin(elem); }
    else if (link == 'register-link') { renderRegister(elem); } 
    else if (link == 'logout-link') { renderLogout(elem); } 
    else if (link == 'change-link') { renderChange(elem); } 
  }

  function renderLogout(elem) {
    let markup =  '<div class="auth-title logout-title">logout</div>' +
                  '<div class="auth-user">' + userName + '</div>' +
                  '<button id="logout-button" class="auth-button">LOGOUT</button>' +
                  '<a id="change-link" class="auth-toggle">change password</a>';
    $(elem).html(markup);
  }

  function renderLogin(elem) {
    let markup =  '<div class="auth-title login-title">login</div>' +
                  '<div class="input-title">USERNAME</div>' +
                  '<input id="input_user" class="auth-input" autofocus>' +
                  '<div class="input-title">PASSWORD</div>' +
                  '<input id="input_password" class="auth-input" type="password">' +
                  '<div class="input-title">REMEMBER ME</div>' +
                  '<input type="checkbox" name="input_remember">' +
                  '<div id="auth-msg"></div>' +
                  '<button id="login-button" class="auth-button">LOGIN</button>' +
                  '<a id="register-link" class="auth-toggle">register</a>';
    $(elem).html(markup);
  }

  function renderRegister(elem) {
    let markup =  '<div class="auth-title register-title">register</div>' +
                  '<div class="input-title">USERNAME</div>' +
                  '<input id="input_name" class="auth-input" autofocus>' +
                  '<div class="input-title">EMAIL</div>' +
                  '<input id="input_email" class="auth-input">' +
                  '<div class="input-title">PASSWORD</div>' +
                  '<input id="input_password" class="auth-input" type="password">' +
                  '<div class="input-title">CONFIRM PASSWORD</div>' +
                  '<input id="input_password_2" class="auth-input" type="password">' +
                  '<div id="auth-msg"></div>' +
                  '<button id="register-button" class="auth-button">REGISTER</button>' +
                  '<a id="login-link" class="auth-toggle">login</a>';
    $(elem).html(markup);
  }

  function renderChange(elem) {
    let markup =  '<div class="auth-title change-title">change password</div>' +
                  '<div class="auth-user">' + userName + '</div>' +
                  '<div class="input-title">NEW PASSWORD</div>' +
                  '<input id="input_password" class="auth-input" type="password">' +
                  '<div class="input-title">CONFIRM NEW PASSWORD</div>' +
                  '<input id="input_password_2" class="auth-input" type="password"><br>' +
                  '<div id="auth-msg"></div>' +
                  '<button id="change-button" class="auth-button">SUBMIT</button><br>' +
                  '<a id="logout-link" class="auth-toggle">logout</a>';
    $(elem).html(markup);
  }

  function renderAuth(elem) {

    let markup = '';
    let auth_div = '#auth-container';

    markup = '<div id="auth-container"></div>'
    $(elem).html(markup);

    if (typeof userName === 'undefined') { renderLogin(auth_div); } // user is not logged in
    else { renderLogout(auth_div); }

  }

