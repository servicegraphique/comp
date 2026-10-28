/* Native replacement for videsigns/webflow-tools multi-step.js.
   Supports the export's data-form, data-answer, data-go-to and data-skip-to
   attributes without a Webflow or CDN runtime. */
(function () {
  'use strict';
  function init(form) {
    var steps = Array.prototype.slice.call(form.querySelectorAll('[data-form="step"]'));
    if (!steps.length) return;
    var history = [0];
    var active = 0;
    function show(index) {
      if (index < 0 || index >= steps.length) return;
      active = index;
      steps.forEach(function (step, i) {
        step.style.display = i === index ? '' : 'none';
        step.setAttribute('aria-hidden', i === index ? 'false' : 'true');
      });
      var first = steps[index].querySelector('input:not([type="hidden"]), select, textarea, button');
      if (first && first.type !== 'submit') first.focus({ preventScroll: true });
    }
    function validateCurrent() {
      var fields = steps[active].querySelectorAll('input, select, textarea');
      for (var i = 0; i < fields.length; i++) {
        var field = fields[i];
        if (field.disabled || field.type === 'hidden' || !field.willValidate) continue;
        if (!field.checkValidity()) {
          field.reportValidity();
          return false;
        }
      }
      return true;
    }
    function targetForNext() {
      var step = steps[active];
      var selected = step.querySelector('input:checked[data-skip-to], input:checked[data-go-to]');
      var direct = selected && (selected.getAttribute('data-skip-to') || selected.getAttribute('data-go-to'));
      var content = step.querySelector('[data-go-to]');
      var route = direct || (content && content.getAttribute('data-go-to'));
      if (route) {
        var exact = steps.findIndex(function (candidate) {
          return Array.prototype.some.call(candidate.querySelectorAll('[data-answer]'), function (el) {
            return el.getAttribute('data-answer') === route;
          });
        });
        if (exact >= 0) return exact;
        var numeric = parseInt(String(route).replace(/^step-/i, ''), 10);
        if (Number.isFinite(numeric) && numeric > 0) return Math.min(numeric - 1, steps.length - 1);
      }
      return Math.min(active + 1, steps.length - 1);
    }
    form.addEventListener('click', function (event) {
      var next = event.target.closest('[data-form="next-btn"]');
      var back = event.target.closest('[data-form="back-btn"]');
      if (!next && !back) return;
      event.preventDefault();
      if (next) {
        if (!validateCurrent()) return;
        var target = targetForNext();
        if (target !== active) history.push(target);
        show(target);
      } else if (history.length > 1) {
        history.pop();
        show(history[history.length - 1]);
      }
    });
    form.addEventListener('change', function (event) {
      var control = event.target;
      if (!control.matches('input[type="radio"][data-radio-skip="true"]')) return;
      var delay = Math.max(0, parseInt(control.getAttribute('data-radio-delay') || '0', 10));
      window.setTimeout(function () {
        if (!control.checked || !steps[active].contains(control) || !validateCurrent()) return;
        var target = targetForNext();
        if (target !== active) history.push(target);
        show(target);
      }, delay);
    });
    show(0);
  }
  function start() {
    document.querySelectorAll('form[data-form="multistep"]').forEach(init);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
})();
