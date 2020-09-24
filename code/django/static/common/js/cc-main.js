  let userData = null;

  // bind listeners for nav links      
  $(document).on('click', '#profile-button', function() { window.location.href = '/app/login/'; });
  $(document).on('click', '#nav-main-map', function() { window.location.href = '/app/map/'; });

  $(document).on('click', '#nav-quote-list', function() { window.location.href = '/app/quotes/'; });
  $(document).on('click', '#nav-quote-create', function() { window.location.href = '/app/quotes/create/'; });

  $(document).on('click', '#nav-order-list', function() { window.location.href = '/app/orders/'; });
  $(document).on('click', '#nav-r1-list', function() { window.location.href = '/app/r1/orders/'; });

  function fetchFromObject(obj, prop) {

      if ((typeof obj === 'undefined') || (obj === null)) {
          return null;
      }

      var _index = prop.indexOf('.')
      if (_index > -1) {
          return fetchFromObject(obj[prop.substring(0, _index)], prop.substr(_index + 1));
      }

      if ((typeof obj[prop] === 'undefined')  || (obj[prop] === null)) {
          return null;
      }

      return obj[prop];
  }

  function fetchStrFromObject(obj, prop) {

    var ret_val = fetchFromObject(obj, prop);

    if (ret_val === null) {
        ret_val = '';
    }

    return ret_val;
  }

  function fetchDiff(new_data, data, prop) {

    var ret_val = false;
    var id = fetchFromObject(data, 'id');
    var val = fetchFromObject(data, prop);
    var new_val = fetchFromObject(new_data, prop);

    if (((typeof new_val === 'object') && (JSON.stringify(val) !== JSON.stringify(new_val))) || // something changed
       ((typeof new_val !== 'object') && (val !== new_val)) || // has gone away
       (id === null)) { // this is being initialised for the first time or after an outage
        if (new_val === null) {
            ret_val = '';
        }
        else {
            ret_val = new_val;
        }

        console.log('diff on ' + prop);
        console.log('types: ' + typeof val + ' - ' + typeof new_val);
        console.log('new val:'); 
        console.log(ret_val);
    }

    return ret_val;
  }

  function sendPost(endPoint, postData) {

    var ret_val =  $.ajax({
      headers: { 'X-CSRFToken': $('meta[name="_token"]').attr('content') },
      type : 'POST',
      url : endPoint,
      data : postData,
      dataType : 'json', // what type of data do we expect back from the server
      encode : true
    })
    .done(function(data) {
      console.log(data);
    }).fail(function(data) {
      console.log(data);
    });

    return ret_val;

  }

  function sendChange(model, id, postData) {

    return sendPost('/api/' + model + '/' + id + '/update/', postData);
  }

  function deleteRecords(model, id) {

    var postData = { 'id' : id };

    ret_val =  $.ajax({
        headers: { 'X-CSRFToken': $('meta[name="_token"]').attr('content') },
        type : 'POST', // define the type of HTTP verb we want to use (POST for our form)
        url : '/api/' + model + '/' + id + '/delete/', // the url where we want to POST
        data : postData, // single item now, we can turn this into an array for bulk later
        dataType : 'json', // what type of data do we expect back from the server
        encode : true
    })
    .done(function(data) {
      console.log(data); // log the result to the console
    })
    .fail(function(data) {
      console.log(data); // log the result to the console
    });

    return ret_val;
  }

  function getStRange(st_num_1, st_num_2) {
    var ret_val = st_num_1;
    if (st_num_2 != '') {
      ret_val += '-' + st_num_2;
    }

    return ret_val;
  }

  function renderHdr(elem) {

    markup =  '<div id="logo-r-div">' +
                '<a href="/"><img src="/static/common/img/mtlogo2.png" class="logo-href"></a>' +
                '<div class="logo-text-div">' +
                  '<div class="logo-title-text">LOC-8</div>' +
                  '<div class="logo-subtitle-text">type-r</div>' +
                '</div>' +
              '</div>' +
              '<button id="profile-button"><i class="far fa-user"></i></button>' +
              '<span class="login-user">' + userName + '</span>';
              //'<span class="login-user">mhulo</span>';

    $(elem).html(markup);
  }

  function getUser(data) {

      return data.email.split('@')[0];
  }

  function formatClassVal(val) {

    ret_val = val.replace(/ |:|mbps|\//gi, '');
    return ret_val;
  }

  function formatCamelVal(val) {
    ret_val = val.replace( /([A-Z])/g, "-$1" );
    ret_val = ret_val.toUpperCase();
    return ret_val;
  }
