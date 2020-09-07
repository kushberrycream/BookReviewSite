$(function () {
  $("#searchForm").submit(function () {
    let search = $("#search").val();
    $(this).attr("action", "/all_books/search/" + search);
    if ($("#search").val() == "")
        $(this).attr("action", "/all_books");
  });
});
