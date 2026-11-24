# Пиццерия на Django: 5 заданий

У нас уже есть: модель `Pizza`, страница меню `/` и админка `/admin`.
Задания идут от простого к сложному. Делай по порядку: следующее опирается на предыдущее.

## Как сдавать

1. Обнови проект и создай свою ветку (имя_фамилия латиницей):
   ```bash
   git checkout main
   git pull
   git checkout -b aman_abdyldaev
   ```
2. Сделал задание, проверил в браузере, сделал коммит:
   ```bash
   git add .
   git commit -m "Задание 1: is_visible"
   ```
   Один коммит на одно задание. Так видно, что ты сделал и в каком порядке.
3. Отправь ветку на GitHub:
   ```bash
   git push -u origin aman_abdyldaev
   ```
   Потом после каждого коммита просто `git push`.

Не забывай про миграции: поменял `models.py`, значит
```bash
python manage.py makemigrations
python manage.py migrate
```
Файлы миграций (`main/migrations/0002_...py`) тоже коммить.

---

## Задание 1. Кнопка «Показывать на сайте»

Иногда пицца закончилась, а удалять её жалко. Сделаем галочку, которая прячет пиццу с сайта.

1. В модель `Pizza` добавь поле:
   ```python
   is_visible = models.BooleanField('Показывать на сайте', default=True)
   ```
2. Сделай миграции.
3. В `views.py` вместо `Pizza.objects.all()` выводи только видимые пиццы. Подсказка: `.filter(...)`.
4. В `admin.py` вместо `admin.site.register(Pizza)` сделай свой класс админки, чтобы в списке пицц были колонки название, цена, «показывать на сайте», и галочку можно было менять прямо в списке:
   ```python
   @admin.register(Pizza)
   class PizzaAdmin(admin.ModelAdmin):
       list_display = [...]
       list_editable = [...]
   ```

**Проверка:** сними галочку у одной пиццы в админке, обнови `/`, её нет. Поставь обратно, она есть.

**Вопросы на сдаче:**
- Зачем `default=True`? Что было бы со старыми пиццами без него?
- Что делает `makemigrations`, а что `migrate`?

---

## Задание 2. Страница одной пиццы

Нажимаешь на название пиццы и попадаешь на её отдельную страницу.

1. В `views.py` новая функция:
   ```python
   def pizza_detail(request, pk):
       pizza = get_object_or_404(Pizza, pk=pk, is_visible=True)
       return render(request, 'pizza_detail.html', {'pizza': pizza})
   ```
   `get_object_or_404` импортируй из `django.shortcuts`.
2. В `config/urls.py` добавь путь `pizza/<int:pk>/` и дай имена всем путям:
   ```python
   path('', index, name='index'),
   path('pizza/<int:pk>/', pizza_detail, name='pizza_detail'),
   ```
3. Создай шаблон `pizza_detail.html`: фото, название, описание, цена и ссылка «← Назад в меню».
4. В `index.html` сделай название пиццы ссылкой. Адрес не пиши руками, используй тег:
   ```html
   <a href="{% url 'pizza_detail' pizza.pk %}">{{ pizza.name }}</a>
   ```

**Проверка:**
- `/pizza/1/` открывает первую пиццу.
- `/pizza/999/` показывает ошибку 404, а не падает с ошибкой 500.
- Скрытая пицца (из задания 1) по прямой ссылке тоже даёт 404.

**Вопросы на сдаче:**
- Откуда функция узнаёт `pk`?
- Чем `{% url 'pizza_detail' pizza.pk %}` лучше, чем написать `/pizza/{{ pizza.pk }}/`?

---

## Задание 3. Общий шаблон и страница «О нас»

Сейчас у каждой страницы свой `<head>`, и меню пришлось бы копировать везде. Вынесем общее в один файл.

1. Создай `main/templates/base.html`. В нём `<head>`, подключение `style.css`, навигация и подвал:
   ```html
   <nav>
       <a href="{% url 'index' %}">Меню</a> |
       <a href="{% url 'about' %}">О нас</a>
   </nav>
   {% block content %}{% endblock %}
   <footer>© Пиццерия</footer>
   ```
   Заголовок вкладки тоже сделай блоком: `<title>{% block title %}Пиццерия{% endblock %}</title>`.
2. Переделай `index.html` и `pizza_detail.html`: первая строка `{% extends 'base.html' %}`, всё содержимое внутри `{% block content %} ... {% endblock %}`. Лишний `<head>` и `<body>` из них убери.
3. На странице пиццы заголовок вкладки должен быть названием пиццы.
4. Сделай страницу `/about/` (view, url с `name='about'`, шаблон): адрес, телефон, часы работы. Она тоже наследует `base.html`.

**Проверка:** на всех трёх страницах одинаковые меню и подвал, а в `index.html` больше нет тега `<head>`.

**Вопросы на сдаче:**
- Что будет, если на странице не написать `{% block title %}`?
- Ты поменял подвал. Сколько файлов пришлось править?

---

## Задание 4. Поиск и сортировка

Добавим на главную форму поиска. Данные из формы приходят в адресной строке: `/?q=Пеп&sort=cheap`.

1. В `index.html` над карточками:
   ```html
   <form method="get">
       <input type="text" name="q" value="{{ q }}" placeholder="Поиск">
       <select name="sort">
           <option value="">Без сортировки</option>
           <option value="cheap">Сначала дешёвые</option>
           <option value="expensive">Сначала дорогие</option>
       </select>
       <button>Найти</button>
   </form>
   ```
2. В `index` достань значения из `request.GET` и примени к запросу:
   ```python
   q = request.GET.get('q', '')
   if q:
       pizzas = pizzas.filter(name__icontains=q)
   ```
   Сортировку сделай сам: `cheap` по возрастанию цены, `expensive` по убыванию. Подсказка: `.order_by('price')` и `.order_by('-price')`.
3. Передай `q` в шаблон, чтобы после поиска текст оставался в поле.
4. Если ничего не нашлось, должна быть надпись «Ничего не найдено» (вспомни `{% empty %}`).

Важно: SQLite ищет без учёта регистра только латиницу. «Пеп» найдёт «Пепперони», а «пеп» нет. Это нормально, не баг твоего кода.

**Проверка:** поиск по части названия работает, сортировка в обе стороны работает, скрытые пиццы в поиске не появляются.

**Вопросы на сдаче:**
- Почему форма `method="get"`, а не `post`?
- Что лежит в `request.GET`, если открыть просто `/`?

---

## Задание 5. Заказ пиццы

Самое главное: пользователь оставляет заказ, а мы видим его в админке.

1. Новая модель в `models.py`:
   ```python
   class Order(models.Model):
       pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
       customer_name = models.CharField(max_length=100)
       phone = models.CharField(max_length=20)
       quantity = models.PositiveIntegerField(default=1)
       created_at = models.DateTimeField(auto_now_add=True)
   ```
   Добавь `__str__`, например `Аман: Пепперони x2`. Сделай миграции и зарегистрируй `Order` в админке с `list_display`.
2. На странице пиццы форма заказа:
   ```html
   <form method="post">
       {% csrf_token %}
       <input name="customer_name" placeholder="Имя">
       <input name="phone" placeholder="Телефон">
       <input name="quantity" type="number" value="1" min="1">
       <button>Заказать</button>
   </form>
   ```
3. В `pizza_detail` обработай отправку:
   ```python
   if request.method == 'POST':
       name = request.POST.get('customer_name', '').strip()
       # достань phone и quantity сам
       # если что-то пустое или quantity меньше 1, покажи ошибку на странице
       # иначе Order.objects.create(...) и redirect('thanks')
   ```
4. Сделай страницу `/thanks/` с текстом «Спасибо! Заказ принят» и ссылкой в меню.

**Проверка:**
- Заказ появляется в админке в разделе Orders.
- Пустое имя или количество 0: заказ не сохраняется, на странице видна ошибка.
- После заказа обнови страницу «Спасибо» (F5). Заказ не должен задвоиться.

**Вопросы на сдаче:**
- Что будет, если убрать `{% csrf_token %}`? Попробуй.
- Зачем после сохранения делать `redirect`, а не сразу `render`?
- Что значит `on_delete=models.CASCADE`? Что станет с заказами, если удалить пиццу?

---

## Для сильных (по желанию, отдельным коммитом)

Категории пицц: модель `Category` (поле `name`), у `Pizza` поле `category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)`. На главной ссылки на категории (`?category=1`) и фильтр по ним, на карточке подпись категории.

## Оценка

Каждое задание 4 балла, всего 20.

| Баллы | Что значит |
|---|---|
| 4 | Работает, все пункты проверки проходят, на вопросы ответил сам |
| 3 | Работает, но мелкая недоделка (нет ссылки назад, нет сообщения об ошибке) |
| 2 | Работает частично или объяснить не смог |
| 0–1 | Не работает или нет коммита |

18–20 = 5, 15–17 = 4, 10–14 = 3, 0–9 = 2.
