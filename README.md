# Мария Путилина — портфолио

Статический сайт-портфолио коммуникационного дизайнера.

- **Стилистика** — по мотивам [core-method.studio](https://core-method.studio/): белое поле, графитовый и серые тексты, плашки-пилюли, плитки 4:5 с подписью по наведению.
- **Подвал** — по схеме [kirstenhumpfer.de](https://www.kirstenhumpfer.de/): фраза и кнопка-пилюля, ниже сетка контактов и нижняя строка; кегли, отступы и колонки — из системы сайта.
- **Главная и «Обо мне»** — структура страниц главной и Info студии Core Method.
- **Кейсы и «Опыт»** — структура кейса и страницы Experience с [bogdan.vision](https://www.bogdan.vision/en/works/be-in-crypto): обложка с заголовком, строка метаданных, «коротко / контекст», нумерованные разделы, ключевые результаты, следующий проект.
- **Контент** — из портфолио в Notion.

## Структура

```
index.html            главная: фильтр + сетка проектов
about.html            обо мне
experience.html       опыт работы, образование, инструменты
works/*.html          6 кейсов: hexway, checkmate, dsec, solisoft, ancor, limoncello
assets/css/style.css  стили
assets/js/main.js     фильтр, появление блоков, инверсия меню над тёмными кадрами
assets/img/           изображения (WebP)
assets/files/         резюме PDF
build/content.py      весь текст сайта
build/build.py        генератор HTML
```

## Как править

HTML-страницы собираются из `build/content.py`. Поменяйте текст там и пересоберите:

```bash
python3 build/build.py
```

Нужен только Python 3, без зависимостей. Размеры картинок лежат в `build/dims.json`. Если добавляете новое изображение, добавьте туда его ширину и высоту.

Локальный просмотр:

```bash
python3 -m http.server 8000
```

## Публикация на GitHub Pages

Settings → Pages → Source: *Deploy from a branch* → ветка `main`, папка `/ (root)`.
