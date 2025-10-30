document.addEventListener('DOMContentLoaded', () => {
  const SHOW_INTERVAL = 24 * 60 * 60 * 1000; // 24 часа

  function saveCookieConsent(consent) {
    const maxAge = 2592000; // 30 дней
    const value = consent ? 'true' : 'false';
    const isLocalhost = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
    const secureFlag = isLocalhost ? '' : '; Secure';

    document.cookie = `cookieConsent=${value}; path=/; max-age=${maxAge}; SameSite=Lax${secureFlag}`;
  }

  function shouldShowCookieBanner() {
    const cookieConsent = document.cookie
      .split('; ')
      .find(row => row.startsWith('cookieConsent='));

    if (!cookieConsent) return true;

    const value = cookieConsent.split('=')[1];
    return value !== 'true' && value !== 'false';
  }

  function createCookieBanner() {
    const consentPopup = document.createElement('div');
    consentPopup.id = 'cookie-consent-popup';
    consentPopup.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: #ccc;
      border-radius: 6px;
      border: 1px solid #ccc;
      padding: 15px;
      z-index: 1000;
    `;

    consentPopup.innerHTML = `
      <p>Для удобства пользователей на сайте мы используем cookies</p>
      <button id="cookie-accept" style="background: #FFD700; border:1px solid #FFD700; border-radius: 6px; font-size: 16px; padding: 4px 8px;">Принять</button>
      <button id="cookie-decline" style="background: #fff; border:1px solid #FFD700; border-radius: 6px; font-size: 16px; padding: 4px 8px;">Отклонить</button>
    `;

    document.body.appendChild(consentPopup);

    const acceptBtn = document.getElementById('cookie-accept');
    const declineBtn = document.getElementById('cookie-decline');

    acceptBtn.addEventListener('click', () => {
      saveCookieConsent(true);
      consentPopup.remove();
    });

    declineBtn.addEventListener('click', () => {
      saveCookieConsent(false);
      consentPopup.remove();
    });
  }

  // ✅ Показываем баннер, если нужно
  if (shouldShowCookieBanner()) {
    createCookieBanner();
  }
});
