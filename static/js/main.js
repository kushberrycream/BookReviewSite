$(function () {
  $("#searchForm").submit(function () {
    let search = $("#search").val();
    $(this).attr("action", "/all_books/");
    if ($("#search").val() == "") $(this).attr("action", "/all_books");
  });
});

// Tooltips Initialization
$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

// popovers Initialization
$(function () {
  $('[data-toggle="popover-hover"]').popover({
    trigger: 'hover',
  })
})

$("ul:last").addClass("d-flex justify-content-center");
