function getBasketFromCookies() {
  try {
    const cookie = document.cookie
      .split('; ')
      .find(row => row.startsWith('basket='));
    const parsed = cookie ? JSON.parse(decodeURIComponent(cookie.split('=')[1])) : {};
    return typeof parsed === 'object' && parsed !== null ? parsed : {};
  } catch (e) {
    console.warn('Ошибка чтения куки basket:', e);
    return {};
  }
}

function saveBasketToCookies(basket) {
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
  document.cookie = 'basket=' + encodeURIComponent(JSON.stringify(basket)) + '; path=/; max-age=2592000';
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
