// Spoločný JS pre oba mockupy (mobilné menu, FAQ accordion klik mimo, withdraw reveal, row expand).
document.addEventListener('DOMContentLoaded', function () {
  var burger = document.getElementById('burgerBtn');
  var nav = document.getElementById('mainNav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      nav.classList.toggle('open');
      burger.classList.toggle('open');
    });
  }

  [['withdrawBtn', 'withdrawCode'], ['withdrawBtnWallet', 'withdrawCodeWallet']].forEach(function (pair) {
    var withdrawBtn = document.getElementById(pair[0]);
    var withdrawCode = document.getElementById(pair[1]);
    if (withdrawBtn && withdrawCode) {
      withdrawBtn.addEventListener('click', function () {
        withdrawCode.classList.add('show');
        withdrawCode.focus();
        withdrawBtn.textContent = 'Potvrdiť výber';
      });
    }
  });

  // Chat bubble widget (globálne na každej stránke)
  var chatBtn = document.getElementById('chatBtn');
  var chatPanel = document.getElementById('chatPanel');
  if (chatBtn && chatPanel) {
    chatBtn.addEventListener('click', function () {
      chatPanel.classList.toggle('open');
    });
  }

  // Slider kalkulačka pôžičky (ziadost-o-uver.html)
  var loanAmount = document.getElementById('loanAmount');
  var loanDays = document.getElementById('loanDays');
  if (loanAmount && loanDays) {
    var loanAmountVal = document.getElementById('loanAmountVal');
    var loanDaysVal = document.getElementById('loanDaysVal');
    var loanRateVal = document.getElementById('loanRateVal');
    var loanTotalVal = document.getElementById('loanTotalVal');
    var loanFeeVal = document.getElementById('loanFeeVal');
    function recalcLoan() {
      var amount = +loanAmount.value;
      var days = +loanDays.value;
      // Úrok klesá s kratšou splatnosťou (19 % pri 15 dňoch – 24 % pri 30 dňoch), p.a.
      var rate = 19 + (days - 15) / (30 - 15) * 5;
      var interest = amount * (rate / 100) * (days / 365);
      var fee = Math.max(20, amount * 0.18 * (days / 30));
      var total = amount + interest + fee;
      loanAmountVal.textContent = amount + ' €';
      loanDaysVal.textContent = days + ' dní';
      loanRateVal.textContent = rate.toFixed(1).replace('.', ',') + ' %';
      loanFeeVal.textContent = fee.toFixed(2).replace('.', ',') + ' €';
      loanTotalVal.textContent = total.toFixed(2).replace('.', ',') + ' €';
    }
    loanAmount.addEventListener('input', recalcLoan);
    loanDays.addEventListener('input', recalcLoan);
    recalcLoan();
  }

  // Slider kalkulačka investície (pre-investorov.html)
  var investAmount = document.getElementById('investAmount');
  var investMonths = document.getElementById('investMonths');
  if (investAmount && investMonths) {
    var investAmountVal = document.getElementById('investAmountVal');
    var investMonthsVal = document.getElementById('investMonthsVal');
    var investRateVal = document.getElementById('investRateVal');
    var investReturnVal = document.getElementById('investReturnVal');
    var investTotalVal = document.getElementById('investTotalVal');
    function recalcInvest() {
      var amount = +investAmount.value;
      var months = +investMonths.value;
      // Výnos rastie s dĺžkou investície (19 % pri 12 mes. – 24 % pri 60 mes.), p.a.
      var rate = 19 + (months - 12) / (60 - 12) * 5;
      var ret = amount * (rate / 100) * (months / 12);
      var total = amount + ret;
      investAmountVal.textContent = amount.toLocaleString('sk-SK') + ' €';
      investMonthsVal.textContent = months + ' mes.';
      investRateVal.textContent = rate.toFixed(1).replace('.', ',') + ' %';
      investReturnVal.textContent = '+' + ret.toFixed(2).replace('.', ',') + ' €';
      investTotalVal.textContent = total.toFixed(2).replace('.', ',') + ' €';
    }
    investAmount.addEventListener('input', recalcInvest);
    investMonths.addEventListener('input', recalcInvest);
    recalcInvest();
  }

  // Viackrokový formulár žiadosti o pôžičku (ziadost-o-uver.html)
  var wizardForm = document.getElementById('wizardForm');
  if (wizardForm) {
    var steps = wizardForm.querySelectorAll('.wizard-step');
    var stepperDots = document.querySelectorAll('.stepper .stepper-step');
    function goToStep(n) {
      steps.forEach(function (step) {
        step.hidden = step.getAttribute('data-step') !== String(n);
      });
      stepperDots.forEach(function (dot, i) {
        dot.classList.remove('active', 'done');
        if (i + 1 < n) dot.classList.add('done');
        else if (i + 1 === n) dot.classList.add('active');
      });
      wizardForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    wizardForm.querySelectorAll('.wizard-next').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var current = parseInt(btn.closest('.wizard-step').getAttribute('data-step'), 10);
        goToStep(current + 1);
      });
    });
    wizardForm.querySelectorAll('.wizard-back').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var current = parseInt(btn.closest('.wizard-step').getAttribute('data-step'), 10);
        goToStep(current - 1);
      });
    });
    wizardForm.addEventListener('submit', function (e) {
      e.preventDefault();
      window.location.href = 'stav-ziadosti.html';
    });
  }

  // Tlačidlo "Uhradiť pôžičku" rozbalí platobné údaje priamo pod pôžičkou
  document.querySelectorAll('.js-toggle-payment').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var target = document.getElementById(btn.getAttribute('data-target'));
      if (!target) return;
      target.classList.toggle('show');
      if (target.classList.contains('show')) {
        target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  });

  // Zmena osobných údajov vyžaduje potvrdenie bezpečnostným kódom
  document.querySelectorAll('.js-confirm-code-form').forEach(function (form) {
    var saveBtn = form.querySelector('.js-save-profile');
    var codeBox = form.querySelector('.security-code-box');
    if (!saveBtn || !codeBox) return;
    saveBtn.addEventListener('click', function (e) {
      e.preventDefault();
      codeBox.classList.add('show');
      codeBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
    var confirmBtn = form.querySelector('.js-confirm-code');
    if (confirmBtn) {
      confirmBtn.addEventListener('click', function (e) {
        e.preventDefault();
        codeBox.classList.remove('show');
        codeBox.classList.add('confirmed');
        confirmBtn.textContent = 'Zmeny uložené ✓';
      });
    }
  });

  // Mobilné rozbaľovacie menu pre sidebar v dashboardoch (dlžník/investor/admin)
  var sidebarToggle = document.getElementById('dashSidebarToggle');
  var sidebar = document.querySelector('.dash-sidebar');
  var sidebarOverlay = document.getElementById('dashSidebarOverlay');
  var sidebarClose = document.getElementById('dashSidebarClose');
  function closeSidebar() {
    if (sidebar) sidebar.classList.remove('open');
    if (sidebarOverlay) sidebarOverlay.classList.remove('show');
  }
  function openSidebar() {
    if (sidebar) sidebar.classList.add('open');
    if (sidebarOverlay) sidebarOverlay.classList.add('show');
  }
  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', openSidebar);
  }
  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeSidebar);
  }
  if (sidebarClose) {
    sidebarClose.addEventListener('click', closeSidebar);
  }
  document.querySelectorAll('.dash-sidebar .sidebar-nav-link').forEach(function (link) {
    link.addEventListener('click', closeSidebar);
  });

  // "Podpora" v sidebar menu dashboardov otvára chat bublinu namiesto toho,
  // aby odhlásilo/presunulo používateľa mimo dashboardu na samostatnú stránku Kontakt.
  document.querySelectorAll('.js-open-support').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      if (chatPanel) {
        chatPanel.classList.add('open');
        chatPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  });

  // Klikateľné dlaždice v dashboarde (napr. "Aktívne pôžičky") rozbalia zoznam nižšie
  document.querySelectorAll('[data-reveal-target]').forEach(function (tile) {
    tile.addEventListener('click', function () {
      var target = document.getElementById(tile.getAttribute('data-reveal-target'));
      if (!target) return;
      document.querySelectorAll('.reveal-panel').forEach(function (p) {
        if (p !== target) p.classList.remove('open');
      });
      target.classList.toggle('open');
      if (target.classList.contains('open')) {
        target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  });
});
