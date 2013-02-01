(function() {

  $(document).ready(function() {
    return console.log('raedy');
  });

  $(".username").on("click", function() {
    var uid;
    uid = $(this).attr('uid');
    $("#prev_leaves .modal-header").html("<h3>Last 3 leaves for " + ($(this).text()) + " </h3>");
    return $.ajax({
      url: '/get_prev_leaves?uid=' + uid,
      success: function(data) {
        var html, key, val;
        html = "<table class='table table-bordered'><tr><th>Start Date</th><th>End Date</th><th>Leave</th><th>Status</th></tr>";
        for (key in data) {
          val = data[key];
          html += "<tr><td> " + (val.start_date.substr(0, 10)) + "</td><td> " + (val.end_date.substr(0, 10)) + "</td><td> " + val.leave + " </td> <td> " + val.status + " </td> </tr>";
        }
        html += "</table>";
        $("#prev_leaves .modal-body").html(html);
        return $("#prev_leaves").modal();
      },
      error: function(err) {
        console.log('err');
        return console.log(err);
      }
    });
  });

}).call(this);
