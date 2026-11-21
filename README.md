# Сайт Тереховой Елены Викторовны — репетитора по математике

![Терехова Елена Викторовна — репетитор по математике](docs/assets/banner.svg)

Сайт-визитка на **MkDocs** с темой **Material for MkDocs**. Внутри — главная страница с офферами, направления подготовки, описание методики, результаты, FAQ и контакты.

**Адрес сайта:** <https://alena-teacher.github.io/about-me/>

## Что внутри

- Адаптивный лендинг с hero-блоком, карточками направлений, форматами занятий и CTA.
- Отдельные страницы: ОГЭ, ЕГЭ, школьная программа 1–11, математика с нуля.
- Методика, результаты, FAQ и контакты.
- Светлая и тёмная темы, поиск по сайту, мобильная навигация.
- Фирменный стиль: индиго → фиолетовый → небесный, тёплый янтарный акцент.
- Плавающая кнопка записи на всех страницах с деликатной периодической анимацией.
- Плавающая кнопка звонка «Позвонить мне» с `tel:`-ссылкой и отдельной анимацией.
- SEO-метатеги, Open Graph, JSON-LD и OG-изображение 1200×630.
- Годы в анонсе и копирайте обновляются автоматически — при сборке и в браузере.
- Автоматическая публикация на GitHub Pages через GitHub Actions.

## Локальный запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# запустить локальный сервер с автообновлением
mkdocs serve

# собрать статический сайт в папку site/
mkdocs build --strict
```

Сайт откроется по адресу <http://127.0.0.1:8000/>.

## Структура проекта

```text
.
├── docs/
│   ├── index.md                 # главная
│   ├── about.md                 # обо мне
│   ├── methodology.md           # как проходят занятия
│   ├── results.md               # результаты и прогресс
│   ├── faq.md                   # вопросы и ответы
│   ├── contacts.md              # контакты
│   ├── programs/                # направления подготовки
│   │   ├── index.md
│   │   ├── oge.md
│   │   ├── ege.md
│   │   ├── school.md
│   │   └── from-scratch.md
│   ├── assets/                  # логотип, аватар, OG-изображение
│   ├── stylesheets/extra.css    # фирменные стили
│   └── javascripts/extra.js     # анимации появления блоков
├── overrides/main.html          # OG-метатеги, JSON-LD, анонс, плавающая CTA
├── overrides/404.html           # кастомная страница «не найдено»
├── hooks/study_year.py          # актуальные годы в анонсе и копирайте
├── tools/make_og.py             # генерация OG-изображения
├── mkdocs.yml
└── requirements.txt
```

## Публикация на GitHub Pages

Репозиторий: <https://github.com/alena-teacher/about-me>

В проекте уже есть workflow `.github/workflows/deploy.yml`. При каждом пуше в `main` он собирает сайт и публикует его в ветку `gh-pages` (через `mkdocs gh-deploy`).

Первая публикация:

```bash
git init
git branch -M main
git remote add origin git@github-alena:alena-teacher/about-me.git
git add .
git commit -m "Сайт репетитора по математике на MkDocs Material"
git push -u origin main
```

После пуша:

1. Откройте **Settings → Actions → General** и убедитесь, что workflow имеет право писать в репозиторий (`Read and write permissions`).
2. Откройте **Settings → Pages**.
3. В разделе **Build and deployment** выберите **Deploy from a branch**.
4. Укажите ветку **gh-pages** и папку **/(root)**, сохраните.
5. Через 1–2 минуты сайт будет доступен по адресу <https://alena-teacher.github.io/about-me/>.

> Ветка `gh-pages` уже создана первым запуском workflow. Если сайт всё ещё отдаёт 404, проверьте, что в **Settings → Pages** выбрана именно эта ветка.

## Обновление OG-изображения

Если меняется аватар или текст на карточке для соцсетей:

```bash
pip install pillow
python tools/make_og.py
```

Скрипт пересоберёт `docs/assets/og-image.png` (1200×630).

## Полезные команды

```bash
# проверить сборку без предупреждений
mkdocs build --strict

# опубликовать в ветку gh-pages вручную (альтернатива Actions)
mkdocs gh-deploy --force
```

## SSH для аккаунта alena-teacher

В `~/.ssh/config` уже настроен отдельный хост:

```sshconfig
Host github-alena
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_alena
  IdentitiesOnly yes
```

Поэтому remote указывается так:

```bash
git remote add origin git@github-alena:alena-teacher/about-me.git
```
