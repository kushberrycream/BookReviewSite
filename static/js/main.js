$(function() {
   $('#searchForm').submit(function(){
     var search = $('#search').val();
     $(this).attr('action', '/all_books/search/' + search);
   });
  });