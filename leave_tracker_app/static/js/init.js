var book_id = parseInt(window.location.pathname.split("/")[3]);
var base_url = "/" + book_id;

$("#voteup").live("click", function(e){
  e.preventDefault();
  url = base_url + "/upvote/";
  $.post(url, {},
         function(data){
           num = parseInt($("#numupvotes").text());
           $("#numupvotes").text(num+1);
           
         });
});

$("#votedown").live("click", function(e){
  e.preventDefault();
  url = base_url + "/downvote/";
  $.post(url, {},
         function(data){
           num = parseInt($("#numdownvotes").text());
           $("#numdownvotes").text(num+1);
           
         });
});

$("#issue").live("click", function(e){
  e.preventDefault();
  url = base_url + "/issue/";
  $.post(url, function(data){
    if (data == "0"){
      alert("The book has already been issued!");
    }
    else{
      alert("Yep! the book is booked in your name.");
      window.location.reload();
    }
  });
});

$("#return").live("click", function(e){
  e.preventDefault();
  url = base_url + "/return/";
  $.post(url, function(data){
    if (data=="0"){
    alert("WTF are you returning! Stop playing around.");
    }
    else{
      alert("Thanks, for returning the book!");
      window.location.reload();
    }
    
  });
});
