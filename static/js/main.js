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
