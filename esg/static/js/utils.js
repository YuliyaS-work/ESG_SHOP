function saveCookieConsent(consent) {
  const maxAge = consent ? 2592000 : 0; // 30 дней или удалить
  document.cookie = `cookieConsent=${consent}; path=/; max-age=${maxAge}`;
}

function getBasketFromCookies() {
  try {
    const cookie = document.cookie
      .split('; ')
      .find(row => row.startsWith('basket='));
    if (!cookie) return {};
    const value = decodeURIComponent(cookie.split('=')[1]);
    const parsed = JSON.parse(value);
    return parsed && typeof parsed === 'object' ? parsed : {};
  } catch (e) {
    console.warn('Ошибка чтения куки basket:', e);
    return {};
  }
}

function saveBasketToCookies(basket) {
    const consentCookie = document.cookie
    .split('; ')
    .find(row => row.startsWith('cookieConsent='));
  const consent = consentCookie ? consentCookie.split('=')[1] === 'true' : false;

  // пересчитываем общую стоимость
  let totalSum = 0;
  Object.entries(basket).forEach(([key, value]) => {
    if (key !== 'generalCost') {
      const [quantity, price] = value;
      totalSum += parseFloat(price);
    }
  });
  basket.generalCost = totalSum.toFixed(2);
  // сохраняем всё в одной куке
   const maxAge = consent ? 2592000 : 0;
  document.cookie = 'basket=' + encodeURIComponent(JSON.stringify(basket)) + '; path=/; max-age=${maxAge}';
}


function clearBasketCookies() {
  document.cookie = 'basket=; path=/; max-age=0';
}


function getCSRFToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) return value;
  }
  return '';
}
