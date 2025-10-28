document.addEventListener('DOMContentLoaded', () => {
  const consentPopup = document.getElementById('cookie-consent-popup');
  const acceptBtn = document.getElementById('cookie-accept');
  const declineBtn = document.getElementById('cookie-decline');

  const consentCookie = document.cookie
    .split('; ')
    .find(row => row.startsWith('cookieConsent='));

  if (!consentCookie) {
    consentPopup.style.display = 'block';
  }

  acceptBtn.addEventListener('click', () => {
    saveCookieConsent(true);
    consentPopup.style.display = 'none';
  });

  declineBtn.addEventListener(
  'click', () => {
    saveCookieConsent(false);
    clearBasketCookies();
    consentPopup.style.display = 'none';
  });
});
