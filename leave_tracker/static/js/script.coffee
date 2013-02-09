$(document).ready ->
  $(".nav li").removeClass("active").find("a[href='#{window.location.pathname}']").closest("li").addClass("active")
