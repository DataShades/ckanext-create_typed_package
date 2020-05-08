jQuery(document).ready(
  (function($, ckan) {
    "use strict";
    var newUrl = "/dataset/new";
    var links = $('[href*="' + newUrl + '"]').filter(function(idx, el) {
      return (
        el.pathname.lastIndexOf(newUrl) == el.pathname.length - newUrl.length
      );
    });

    if (!links.length) {
      return;
    }
    var modal = $(
      [
        '<div class="modal fade">',
        '<div class="modal-dialog">',
        '<div class="modal-content">',
        '<div class="modal-header">',
        '<button type="button" class="close" data-dismiss="modal">×</button>',
        '<h3 class="modal-title"></h3>',
        "</div>",
        '<div class="modal-body">',

        '<div class="control-group form-group control-medium">',
        '<label for="field-ctp-package-type" class="control-label"></label>',
        '<div class="controls">',
        '<select id="field-ctp-package-type" class="form-control">',
        "</select>",
        "</div>",
        "</div>",

        "</div>",
        '<div class="modal-footer">',
        '<button class="btn btn-default btn-cancel" data-dismiss="modal"></button>',
        '<button class="btn btn-primary"></button>',
        "</div>",
        "</div>",
        "</div>",
        "</div>"
      ].join("\n")
    ).modal({ show: false });

    modal.find(".modal-title").text(ckan.i18n._("Please Select Type"));
    modal.find(".control-label").text(ckan.i18n._("Type"));
    modal
      .find(".btn-primary")
      .text(ckan.i18n._("Confirm"))
      .on("click", function() {
        var type = modal.find("#field-ctp-package-type").val();
        var url = ckan.url(type + "/new");
        window.location.href = url;
      });
    modal.find(".btn-cancel").text(ckan.i18n._("Cancel"));

    var sandbox = new ckan.sandbox(modal);
    sandbox.client.call("GET", "ctp_list_types", "?with_labels=true", function(
      data
    ) {
      if (!data.success) {
        console.error("Type listing: %o", data);
        return;
      }
      var select = modal.find("#field-ctp-package-type");
      data.result.forEach(function(type) {
        $("<option>", { value: type.name, text: type.label }).appendTo(select);
      });
    });

    links.on("click", function(e) {
      e.preventDefault();
      modal.modal("show");
    });
  })(jQuery, ckan)
);
