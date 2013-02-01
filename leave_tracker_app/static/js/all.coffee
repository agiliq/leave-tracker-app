$(document).ready ->
  console.log 'raedy'

$(".username").on "click",  ->
  uid = $(@).attr 'uid'
  $("#prev_leaves .modal-header").html "<h3>Last 3 leaves for #{$(@).text()} </h3>"
  $.ajax
    url: '/get_prev_leaves?uid='+uid,
    success: (data) ->
      html = "<table class='table table-bordered'><tr><th>Start Date</th><th>End Date</th><th>Leave</th><th>Status</th></tr>"
      for key, val of data
        html += "<tr><td> #{val.start_date.substr(0, 10)}</td><td> #{val.end_date.substr(0, 10) }</td><td> #{val.leave} </td> <td> #{val.status} </td> </tr>"
      html += "</table>"
      $("#prev_leaves .modal-body").html html


      $("#prev_leaves").modal()

    error: (err) ->
      console.log 'err'
      console.log err



