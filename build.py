#!/usr/bin/env python3
"""Generate the static Bread & Breakfast site. Usage: build.py OUT_DIR"""
import sys, os, json

OUT = sys.argv[1]
U = "https://breadandbreakfast.co.il/wp-content/uploads/sites/35/"
# Every image the site uses: local path -> original URL (download-images.sh fetches them)
IMAGES = {}
def img(rel):
    local = "images/" + rel.replace("/", "-")
    IMAGES[local] = U + rel
    return "/" + local

LOGO = img("2019/12/logo-03.png")
LOGO_SMALL = img("2019/12/cropped-logo-04-78x51.png")
LOGO_WHITE = img("2019/12/logowhite-01.png")
FAVICON = img("2019/12/cropped-logo-01-270x270.png")
HERO = img("2019/11/1-01.png")
COFFEE = img("2019/11/2-06.png")
ICON = img("2019/11/icon-07.png")
LOGO4 = img("2019/12/logo-04.png")
HERO_SLIDES = [img("2019/12/" + f) for f in ("bg_0019_258A2090.jpg", "bg_0016_258A2008.jpg", "bg_0010_258A2380.jpg", "bg_0005_258A2410.jpg")]
COFFEE_BG = img("2019/11/2_0000__MG_0481.jpg")
MENU_BG = img("2019/12/bg_0004_258A2338.jpg")
FOOTER_BG = img("2019/12/bg_0008_258A2446.jpg")
# Photo banner at the top of inner pages, as on the original site
BANNERS = {
    "/about/": img("2020/02/about.jpg"),
    "/breadandbreakfast_menu/": img("2019/12/bg_0014_258A2023.jpg"),
    "/menu_eng/": img("2019/12/bg_0014_258A2023.jpg"),
    "/event/": img("2020/02/events.jpg"),
    "/company/": img("2019/12/bg2_0003_258A2052.jpg"),
    "/jobs/": img("2019/12/bg2_0006_bread_and_breakfast__86.jpg"),
    "/contact/": img("2019/12/bg2_0003_258A2052.jpg"),
}

WOLT = "https://wolt.com/he/isr/hasharon/restaurant/bread-breakfast-raanana"
MAPS = "https://g.page/bnbreakfast?share"
WAZE = "https://www.waze.com/he/livemap/directions/israel/center-district/raanana/%D7%91%D7%A8%D7%93-%D7%90%D7%A0%D7%93-%D7%91%D7%A8%D7%A7%D7%A4%D7%A1%D7%98-bread-and-breakfast?place=ChIJk-ovmhI4HRURC1-Mr70MzH0"
FB = "https://www.facebook.com/Bread.Breakfast.Coffee/"
IG = "https://www.instagram.com/bread.breakfast.coffee/"
PHONE = "09-772-8340"
ADDRESS = "מרכז גירון, ז'בוטינסקי 3, רעננה"
HOURS = [("ראשון – חמישי", "07:00 – 19:00"), ("שישי", "07:00 – 14:00"), ("שבת", "סגור")]

NAV = [
    ("/", "דף הבית"),
    (WOLT, "משלוחים"),
    ("/about/", "אודות"),
    ("/breadandbreakfast_menu/", "תפריט המסעדה"),
    ("/gallery/", "גלריה"),
    ("/event/", "אירועים"),
    ("/company/", "ליווי עיסקי"),
    ("/jobs/", "דרושים"),
    ("/contact/", "צרו קשר"),
    ("/menu_eng/", "English Menu"),
]

def ext(href):
    return ' target="_blank" rel="noopener"' if href.startswith("http") else ""

KITCHEN_NOTE = "המטבח החם פתוח עד 15:00. אחר כך מחכה לכם ויטרינה עשירה של כריכים, מאפים, סלטים ועוד."
def hours_html():
    rows = "".join(f"<li><span>{d}</span><span dir='ltr'>{h}</span></li>" for d, h in HOURS)
    return rows + f'<li class="note">{KITCHEN_NOTE}</li>'

def page(path, title, body, desc="ברד אנד ברקפסט רעננה – בית למפגש, קפה וארוחות בוקר. כשר למהדרין."):
    nav = "".join(
        f'<li><a href="{h}"{ext(h)}{" aria-current=\"page\"" if h == path else ""}>{t}</a></li>' for h, t in NAV)
    if path in BANNERS:
        body = f'<div class="banner" style="background-image:url({BANNERS[path]})"></div>' + body
    html = f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alef:wght@400;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<a class="skip" href="#main">דילוג לתוכן</a>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="/"><img src="{LOGO_SMALL}" alt="ברד אנד ברקפסט – דף הבית" width="78" height="51"></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">תפריט</button>
    <nav id="site-nav" aria-label="ניווט ראשי"><ul>{nav}</ul></nav>
    <a class="btn btn-order" href="{WOLT}" target="_blank" rel="noopener">הזמינו משלוח</a>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer" style="background-image:url({FOOTER_BG})">
  <div class="wrap footer-top">
    <img src="{LOGO4}" alt="" class="footer-logo" loading="lazy">
    <p class="footer-title" lang="en" dir="ltr">Bread &amp; Breakfast</p>
    <p>ברד אנד ברקפסט<br>{ADDRESS}<br>טלפון: <a href="tel:097728340">{PHONE}</a></p>
  </div>
  <div class="wrap footer-grid">
    <div>
      <h2>שעות פעילות</h2>
      <ul class="hours">{hours_html()}</ul>
    </div>
    <div>
      <ul class="links">
        <li><a href="{MAPS}" target="_blank" rel="noopener">מיקום</a></li>
        <li><a href="{WAZE}" target="_blank" rel="noopener">Waze</a></li>
        <li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li>
        <li><a href="{IG}" target="_blank" rel="noopener">Instagram</a></li>
      </ul>
    </div>
    <div>
      <ul class="links">
        <li><a href="/accessibility/">הצהרת נגישות</a></li>
        <li><a href="/privacy/">מדיניות פרטיות</a></li>
        <li><a href="/terms/">תקנון</a></li>
      </ul>
    </div>
  </div>
  <p class="copy wrap">© כל הזכויות שמורות למסעדת ברד אנד ברקפסט רעננה.</p>
</footer>
<div class="cookie" id="cookie" hidden>
  <p>האתר שלנו משתמש בקוקיז כדי להבטיח חוויית גלישה חלקה, לנתח שימוש באתר ולהתאים תוכן ושירותים אישיים עבורך. <a href="/privacy/">מדיניות פרטיות</a></p>
  <button class="btn" id="cookie-ok">אישור</button>
</div>
<button class="a11y-toggle" aria-expanded="false" aria-controls="a11y-panel" aria-label="תפריט נגישות">♿</button>
<div class="a11y-panel" id="a11y-panel" hidden role="dialog" aria-label="תפריט נגישות">
  <h2>נגישות</h2>
  <button data-a11y="font-up">הגדלת טקסט</button>
  <button data-a11y="font-down">הקטנת טקסט</button>
  <button data-a11y="contrast">ניגודיות גבוהה</button>
  <button data-a11y="mono">מונוכרום</button>
  <button data-a11y="readable">גופן קריא</button>
  <button data-a11y="links">הדגשת קישורים</button>
  <button data-a11y="headings">הדגשת כותרות</button>
  <button data-a11y="cursor">סמן גדול</button>
  <button data-a11y="motion">עצירת אנימציות</button>
  <button data-a11y="reset">איפוס</button>
  <a href="/accessibility/">הצהרת נגישות</a>
</div>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""
    d = os.path.join(OUT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    # Relative links so the site works both on a test sub-path and on the real domain
    depth = len([x for x in path.strip("/").split("/") if x])
    pre = "../" * depth or "./"
    html = html.replace('href="/', 'href="' + pre).replace('src="/', 'src="' + pre).replace('url(/', 'url(' + pre)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

def form(fields, form_id):
    rows = []
    for name, label, typ in fields:
        req = "" if typ.endswith("?") else " required"
        typ = typ.rstrip("?")
        fid = f"{form_id}-{name}"
        if typ == "textarea":
            ctrl = f'<textarea id="{fid}" name="{label}" rows="4"{req}></textarea>'
        elif typ == "radio-exp":
            ctrl = (f'<span class="choices"><label><input type="radio" name="{label}" value="יש לי ניסיון"> יש לי ניסיון</label>'
                    f'<label><input type="radio" name="{label}" value="אני סטודנט"> אני סטודנט</label></span>')
            rows.append(f'<div class="field"><span class="label">{label}</span>{ctrl}</div>')
            continue
        else:
            ctrl = f'<input id="{fid}" name="{label}" type="{typ}"{req}>'
        rows.append(f'<div class="field"><label for="{fid}">{label}</label>{ctrl}</div>')
    return f"""<form class="lead-form" data-form="{form_id}" method="post" action="https://api.web3forms.com/submit">
  <input type="hidden" name="access_key" value="WEB3FORMS_KEY">
  <input type="hidden" name="subject" value="פנייה מהאתר: {form_id}">
  {''.join(rows)}
  <label class="check"><input type="checkbox" name="עדכונים" value="כן"> אשמח לקבל עדכון על הטבות מיוחדות לפרטי ההתקשרות שמסרתי</label>
  <label class="check"><input type="checkbox" required> אני מאשר/ת את <a href="/terms/">תקנון</a> ו<a href="/privacy/">מדיניות פרטיות</a></label>
  <button class="btn" type="submit">שליחה</button>
  <p class="form-ok" hidden role="status">ההודעה נשלחה בהצלחה !</p>
</form>"""

def info_block():
    return f"""<aside class="info">
  <h2>ברד אנד ברקפסט רעננה</h2>
  <p>{ADDRESS}</p>
  <p><strong>טלפון:</strong> <a href="tel:097728340">{PHONE}</a></p>
  <h3>שעות פעילות</h3>
  <ul class="hours">{hours_html()}</ul>
  <p class="social"><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a></p>
</aside>"""

# ---------- Home ----------
HOME_GALLERY = ["2020/02/g_MG_8709.jpg", "2020/02/g_MG_8711.jpg", "2020/02/g_MG_8728.jpg", "2020/02/g_MG_8676.jpg",
                "2020/02/g_MG_8687.jpg", "2020/02/g_MG_8719.jpg", "2020/02/g_MG_8767.jpg", "2020/02/g_MG_8696.jpg"]
home_gal = "".join(f'<img src="{img(p)}" alt="" loading="lazy">' for p in HOME_GALLERY)
page("/", "ברד אנד ברקפסט רעננה | בית למפגש, קפה וארוחות בוקר", f"""
<section class="hero">
  <div class="hero-slides" aria-hidden="true">{''.join(f'<span style="background-image:url({u})"></span>' for u in HERO_SLIDES)}</div>
  <div class="wrap hero-text">
    <img src="{HERO}" alt="" class="hero-img">
    <p class="hero-name" lang="en" dir="ltr">Bread &amp; Breakfast</p>
    <h1>בית למפגש, קפה וארוחות בוקר</h1>
    <p class="kosher">כשר למהדרין</p>
    <a class="btn" href="{WOLT}" target="_blank" rel="noopener">הזמינו משלוח</a>
  </div>
</section>
<section class="band">
  <div class="wrap prose center">
    <img src="{LOGO}" alt="" class="icon" loading="lazy">
    <h2>ברד אנד ברקפסט</h2>
    <p>התפריט העשיר והמגרה של ברד אנד ברקפסט עושה כבוד לארוחת הבוקר במשך כל שעות היום.<br>
    שקשוקות, גבינות, ביצים, מאפים טריים ומגוונים, סנדוויצ'ים וסלטים עשירים לצד פסטות ומנות עיקריות.<br>
    תפריט צמחוני-חלבי שמציע משהו טעים לכל אחד.</p>
    <a class="btn" href="/about/">קראו עוד</a>
  </div>
</section>
<section class="duo">
  <div class="duo-text">
    <img src="{COFFEE}" alt="" class="icon" loading="lazy">
    <h2>על הקפה שלנו</h2>
    <p>רוצים את הקפה של ברד אנד ברקפסט גם בבית?<br>תערובת הבית שלנו וסוגים שונים של קפה חד-זני מרחבי העולם שאנו קולים מידי יום מחכים לכם בחנות</p>
  </div>
  <div class="duo-img" style="background-image:url({COFFEE_BG})"></div>
</section>
<section class="duo">
  <div class="duo-img" style="background-image:url({MENU_BG})"></div>
  <div class="duo-text">
    <img src="{ICON}" alt="" class="icon" loading="lazy">
    <h2>תפריט ברד אנד ברקפסט</h2>
    <p>עם התפריט הצמחוני-חלבי העשיר והמפנק של ברד אנד ברקפסט כל יום יתחיל עם חיוך</p>
    <a class="btn btn-light" href="/breadandbreakfast_menu/">לצפייה בתפריט</a>
  </div>
</section>
<section class="strip" aria-label="תמונות מהמסעדה"><div class="strip-row">{home_gal}</div></section>
<section class="band">
  <div class="wrap center contact-home">
    <h2>צרו קשר</h2>
    <p class="contact-name">ברד אנד ברקפסט רעננה</p>
    <p class="contact-addr">{ADDRESS}</p>
    <ul class="hours">{hours_html()}</ul>
    <p class="social"><a href="{MAPS}" target="_blank" rel="noopener">מיקום</a> · <a href="{WAZE}" target="_blank" rel="noopener">Waze</a> · <a href="tel:097728340">{PHONE}</a></p>
    <a class="btn" href="{WOLT}" target="_blank" rel="noopener">הזמינו משלוח</a>
  </div>
</section>
""")

# ---------- About ----------
ABOUT = [
 "בואו נסכים על דבר אחד – ארוחת בוקר עשירה היא הארוחה הכי כיפית של היום, ואצלנו מאמינים שאין סיבה שלא להזמין אותה גם לצהריים או לערב.",
 "תפריט ברד אנד ברקפסט כשר מהדרין בהשגחת הרבנות, ומציע לכם מבחר גדול של ארוחות בוקר שמשלבות לחם טרי, ביצים כבקשתכם, גבינות, ירקות ועוד מאזטים טעימים – כל אבות המזון ומגוון של טעמים בארוחה אחת. לצד אלו תמצאו כאן שקשוקות מצוינות ומאפים מעלפים.",
 "קחו כמה מנות לדוגמא: \"מאפה עלמוני\" הוא בצק עלים שבתוכו מתערבבים בכיף גבינות פטה ומנצ'גו, ביצה עלומה ורוטב שמנת ותרד. \"אגדת יער\" היא מחבת לוהטת שבה מיקס פטריות עם ביצה עלומה וגבינת פרמזן. שקשוקת פופאי שלנו כוללת שתי ביצים טריות על בסיס תרד ברוטב רויאל וגבינת מוצרלה. אתם כבר מריירים?",
 "הפרנץ' טוסט המושחת שלנו הוא בריוש מטוגן בחמאה ומוגש לצד גלידת וניל או סלט פירות מתוק ומרענן.",
 "ועוד לא הזכרנו את מבחר הלחמים הטריים שלנו, שכולם עשויים מחמצת טבעית ללא שמרים וסוכר, וממש מתחננים שתמרחו עליהם חמאה רכה. הלחמים שלנו הם גם הבסיס לסנדוויצ'ים המצוינים והנדיבים שלנו, שממולאים בגבינות, ירקות, דגים וממרחים מגוונים.",
 "התפריט שלנו כולל גם סלטים עשירים, פסטות בהרכבה ומנות עיקריות מיוחדות למי שלא מוותר על מנה עיקרית חמה לצהריים: חריימה, גירוס שווארמת דג, תבשיל אורז, ירקות וטופו ועוד.",
 "אוהבים פיצה? אתם יכולים לבחור כאן בין מרגריטה קלאסית לפיצה אלפרדו עם ראגו פטריות.",
 "את כל אלו תוכלו לקנח במבחר העוגות והעוגיות שלנו, וללוות לצד אייסים מתוקים על בסיס פירות או חלב או משקאות חמים.",
 "בכל בוקר אנו מכינים לכבודכם מבחר משתנה של עוגות ומאפים טריים, ואתם מוזמנים לשאול אותנו על הספיישלים של היום. המראה של הוויטרינה שלנו בוודאי יקשה עליכם להחליט מה לבחור, אבל אנחנו כאן כדי לעזור לכם ולהמליץ על מה שיהיה לטעמכם.",
 "נשמח לראות ולהאכיל אתכם כבר היום!",
 "שיהיה לכם בתיאבון!",
]
team = "".join(f'<figure><img src="{img("2020/02/" + f + ".jpg")}" alt="{n}" loading="lazy"><figcaption>{n}</figcaption></figure>'
               for f, n in [("ron", "רון"), ("oshik", "אושיק"), ("gil", "גיל")])
page("/about/", "קצת עלינו | ברד אנד ברקפסט רעננה", f"""
<section class="band page-head"><div class="wrap"><h1>קצת עלינו</h1></div></section>
<section class="band"><div class="wrap prose">
  <h2 lang="en" dir="ltr">Bread &amp; Breakfast</h2>
  {''.join(f'<p>{p}</p>' for p in ABOUT)}
  <a class="btn" href="{WOLT}" target="_blank" rel="noopener">הזמינו משלוח</a>
</div></section>
<section class="band alt"><div class="wrap team">{team}</div></section>
""")

# ---------- Menus ----------
MENU_CATS = ["ראשונות וארוחות בוקר", "כריכים וטוסטים", "צהריים וסלטים", "פיצה פסטה ומשקאות", "קינוחים"]
m1, m2, pizza = img("2023/05/menu_page_1.jpg"), img("2023/05/menu_page_2.jpg"), img("2025/02/pizza.jpg")
page("/breadandbreakfast_menu/", "תפריט המסעדה | ברד אנד ברקפסט רעננה", f"""
<section class="band page-head"><div class="wrap"><h1>תפריט ברד אנד ברקפסט</h1>
<p class="cats">{' · '.join(MENU_CATS)}</p></div></section>
<section class="band"><div class="wrap menu-pages">
  <a href="{m1}"><img src="{m1}" alt="תפריט ברד אנד ברקפסט – עמוד 1"></a>
  <a href="{m2}"><img src="{m2}" alt="תפריט ברד אנד ברקפסט – עמוד 2"></a>
  <a href="{pizza}"><img src="{pizza}" alt="תפריט פיצות" loading="lazy"></a>
</div></section>
""")
e1, e2 = img("2023/05/menu_page_eng.jpg"), img("2023/05/menu_page_2-menu_page_eng.jpg")
page("/menu_eng/", "English Menu | Bread & Breakfast Ra'anana", f"""
<section class="band page-head"><div class="wrap" lang="en" dir="ltr"><h1>English Menu</h1>
<p>Bread &amp; Breakfast · Giron Center, 3 Jabotinsky St., Ra'anana</p></div></section>
<section class="band"><div class="wrap menu-pages">
  <a href="{e1}"><img src="{e1}" alt="Bread &amp; Breakfast menu, page 1" lang="en"></a>
  <a href="{e2}"><img src="{e2}" alt="Bread &amp; Breakfast menu, page 2" lang="en"></a>
</div></section>
""")

# ---------- Gallery ----------
GAL = ["2019/12/g_0008_258A2442.jpg", "2019/11/2_0002_bread_and_breakfast__26.jpg", "2019/11/2_0000__MG_0481.jpg",
 "2019/11/2_0003_bread_and_breakfast__17.jpg", "2019/12/g_0001_258A2024.jpg", "2019/12/g_0003_258A2468.jpg",
 "2019/12/g_0040_258A2080.jpg", "2019/12/g_0039_258A2117.jpg", "2019/12/g_0037_258A2133.jpg", "2019/12/g_0004_258A2448.jpg",
 "2019/12/g_0035_258A2164.jpg", "2019/12/g_0030_258A2233.jpg", "2019/12/g_0045_258A2032.jpg", "2019/12/g_0029_258A2237.jpg",
 "2019/12/g_0026_258A2274.jpg", "2019/12/g_0022_258A2345.jpg", "2019/12/g_0043_258A2044.jpg",
 "2019/11/2_0001_bread_and_breakfast__75.jpg", "2019/12/g_0015_258A2401.jpg", "2019/12/g_0014_258A2410.jpg",
 "2019/11/2_0004_bread_and_breakfast__13.jpg", "2019/12/g_0044_258A2036.jpg", "2019/12/g_0046_258A2005.jpg",
 "2019/12/g_0006_258A2445.jpg"]
gal = "".join(f'<a href="{img(p)}"><img src="{img(p)}" alt="" loading="lazy"></a>' for p in GAL)
page("/gallery/", "גלריה | ברד אנד ברקפסט רעננה", f"""
<section class="band page-head"><div class="wrap"><h1>גלריה</h1>
<a class="btn" href="{WOLT}" target="_blank" rel="noopener">הזמינו משלוח</a></div></section>
<section class="band"><div class="wrap gallery">{gal}</div></section>
""")

# ---------- Forms pages ----------
BASE = [("name", "שם מלא", "text"), ("email", "דואר אלקטרוני", "email"), ("phone", "טלפון", "tel")]
def form_page(path, title, h1, intro, fields, fid, extra=""):
    page(path, f"{title} | ברד אנד ברקפסט רעננה", f"""
<section class="band page-head"><div class="wrap"><h1>{h1}</h1><p>{intro}</p></div></section>
<section class="band"><div class="wrap form-split">{form(fields, fid)}{info_block()}{extra}</div></section>
""")

form_page("/event/", "אירועים", "אירועים ברעננה", "רוצים לבוא לחגוג איתנו? אירועים אפשר לקיים גם בערב, עד 22:00. השאירו פרטים ונחזור אליכם בהקדם",
          BASE + [("date", "תאריך האירוע", "date"), ("time", "שעה מבוקשת", "time"),
                  ("guests", "מספר מוזמנים", "number"), ("more", "פרטים נוספים", "textarea?")], "event")
form_page("/company/", "ליווי עסקי", "ליווי עסקי", "השאירו פרטים ונחזור אליכם בהקדם",
          BASE + [("area", "אזור מגורים", "text?"), ("msg", "הודעה", "textarea?")], "company")
form_page("/jobs/", "דרושים", "דרושים עובדים",
          "ברד אנד ברקפסט מחפשים עובדים חייכנים וחרוצים. חושבים שאתם מתאימים? השאירו פרטים ונחזור אליכם בהקדם",
          BASE + [("exp", "ניסיון", "radio-exp"), ("more", "פרטים נוספים", "textarea?")], "jobs")
form_page("/contact/", "צרו קשר", "צרו קשר", f'<a class="btn" href="{WOLT}" target="_blank" rel="noopener">הזמינו משלוח</a>',
          BASE + [("msg", "הודעה", "textarea?")], "contact", extra="""
<aside class="info">
  <h2>נגישות המסעדה</h2>
  <p>יש דלת נגישה | יש רצף נגיש | יש ריהוט נגיש | יש שירותי נכים | יש חניית נכים | אין לולאת השראה</p>
  <p>טלפון אחראי נגישות: אשר <a href="tel:0547707746">054-7707746</a></p>
</aside>""")

# ---------- Legal ----------
page("/accessibility/", "הצהרת נגישות | ברד אנד ברקפסט רעננה", f"""
<section class="band page-head"><div class="wrap"><h1>הצהרת נגישות</h1></div></section>
<section class="band"><div class="wrap prose">
<p>אנו רואים חשיבות רבה במתן שירות שוויוני לכלל הלקוחות, ופועלים כדי שהאתר יהיה נגיש לאנשים עם מוגבלות בהתאם לתקן הישראלי ת"י 5568 ברמה AA.</p>
<h2>כיצד הופכים את האתר לנגיש?</h2>
<p>באתר מוצב כפתור נגישות. לחיצה עליו פותחת תפריט שבו ניתן להגדיל ולהקטין טקסט, להפעיל ניגודיות גבוהה ומונוכרום, לעבור לגופן קריא, להדגיש קישורים וכותרות, להגדיל את הסמן ולעצור אנימציות. האתר מותאם לניווט במקלדת ולקוראי מסך, ולתמונות יש תיאור טקסטואלי.</p>
<h2>נגישות המסעדה</h2>
<p>יש דלת נגישה | יש רצף נגיש | יש ריהוט נגיש | יש שירותי נכים | יש חניית נכים | אין לולאת השראה</p>
<h2>פניות בנושא נגישות</h2>
<p>נתקלתם בבעיה? נשמח לשמוע. אחראי נגישות: אשר, טלפון <a href="tel:0547707746">054-7707746</a>, או דרך <a href="/contact/">טופס יצירת הקשר</a>.</p>
<p class="muted">עודכן לאחרונה: נובמבר 2026</p>
</div></section>
""")
for p, t in [("/privacy/", "מדיניות פרטיות"), ("/terms/", "תקנון")]:
    page(p, f"{t} | ברד אנד ברקפסט רעננה", f"""
<section class="band page-head"><div class="wrap"><h1>{t}</h1></div></section>
<section class="band"><div class="wrap prose"><p class="todo">[טקסט {t} – להעתיק מהאתר הקיים / לנסח לפני העלייה לאוויר]</p></div></section>
""")

with open(os.path.join(OUT, "images.json"), "w", encoding="utf-8") as f:
    json.dump(IMAGES, f, ensure_ascii=False, indent=1)
with open(os.path.join(OUT, "download-images.sh"), "w") as f:
    f.write("#!/bin/sh\n# Downloads every image from the current site into ./images\nset -e\ncd \"$(dirname \"$0\")\"\nmkdir -p images\n")
    for local, url in sorted(IMAGES.items()):
        f.write(f'curl -fsSL -o "{local}" "{url}"\n')
print(len(IMAGES), "images")
