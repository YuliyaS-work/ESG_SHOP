document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.catalog-btn');
  const output = document.getElementById('subrubric-list');
  let subrubrics = {};

  fetch('api/subrubrics/')  // замени на свой URL
    .then(response => response.json())
    .then(data => {
      subrubrics = data;
      console.log('Загруженные данные:', subrubrics);

      const rubricMap = {
        'Электрика': 'subrubrics_electro',
        'Газовое оборудование': 'subrubrics_gas',
        'Сантехника': 'subrubrics_santeh'
      };

      buttons.forEach(button => {
        button.addEventListener('click', () => {
          const rubric = button.dataset.rubric;
          const key = rubricMap[rubric];
          const items = subrubrics[key] || [];

          output.innerHTML =`<ul>` +
            items.map(item => `<li> <a href="${item.rubric}/${item.id}/">${item.title}</li>`).join('') +
            `</ul>`;
        });
      });
    })
    .catch(error => {
      console.error('Ошибка загрузки данных:', error);
    });
});

