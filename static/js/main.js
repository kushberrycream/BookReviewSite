// Tooltips Initialization
$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

// popovers Initialization
$(function () {
  $('[data-toggle="popover-hover"]').popover({
    trigger: "hover",
  });
});

// Adds flexbox classes to pagination when it is available.
$("ul:last").addClass("d-flex justify-content-center");

