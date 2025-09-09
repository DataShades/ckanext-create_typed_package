ckan.module("ctp-type-selector", function ($, _) {
  return {
    links: null,
    options: {
      newUrl: "/dataset/new",
      ignoreSelector: "[data-ctp-ignore]",
    },

    modal: null,
    query: "",

    initialize: function () {
      const self = this;

      const url = this.options.newUrl;
      const id = "ctp-type-selector-modal";
      const modalEl = document.getElementById(id);
      if (!modalEl) {
        console.warning(
          "[create-typed-package] Cannot locate modal with ID %s",
          id,
        );
        return;
      }

      const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
      const field = document.getElementById("field-ctp-package-type");

      const links = $('[href*="' + url + '"]')
        .not(this.options.ignoreSelector)
        .filter(function (idx, el) {
          return (
            el.pathname.lastIndexOf(url) == el.pathname.length - url.length
          );
        });
      if (!links.length) {
        return;
      }

      modalEl.querySelector(".ctp-confirm").addEventListener("click", () => {
        const type = field.value;
        this.goTo(type);
      });

      links.on("click", function (e) {
        var currentLink = $(this);
        e.preventDefault();

        self.query = currentLink.prop("search");

        if (field.options.length === 1) {
          self.goTo(field.options[0].value);
        } else {
          modal.show();
          modalEl.addEventListener("hidden.bs.modal", function () {
            currentLink.focus();
          });
        }
      });
    },

    goTo(type) {
      const url = ckan.url(type + "/new") + this.query;
      window.location.href = url;
    },
  };
});
