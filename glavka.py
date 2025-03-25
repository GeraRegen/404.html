html_content = """

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Тревога</title>
    <style>
        .info-container_1 {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-image: url('about2.jpg');
            background-size: cover;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #000;
            text-align: justify;
        }
        .info-container_1 h2 {
            color: #000;
            margin-top: 0;
            text-align: center;
        }
        .cloud-glava {
            width: 100%;
            background-image: url('oblako.jpg');
            background-size: cover;
            border-radius: 0 0 20px 20px;
            padding: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }
        nav {
            background-color: #333;
            padding: 10px;
            text-align: center;
        }
        nav a {
            color: white;
            margin: 0 15px;
            text-decoration: none;
            font-weight: bold;
        }
        nav a:hover {
            text-decoration: underline;
        }
        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 20px;
            width: 100%;
        }
        img {
            max-width: 100%;
            height: auto;
            margin: 10px auto;
            display: block;
        }
        .cloud-container {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            margin: 20px 0;
        }
        .cloud-box {
            width: 30%;
            min-width: 250px;
            background-color: #63b3ed;
            background-image: linear-gradient(to bottom, #63b3ed, #4a90e2);
            border-radius: 20px;
            padding: 20px;
            color: white;
            margin: 10px 0;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .cloud-box a {
            color: white;
            text-decoration: none;
        }
        pre {
            white-space: pre-wrap;
            font-family: Arial, sans-serif;
            margin: 10px auto;
            max-width: 800px;
        }
        @media (max-width: 768px) {
            .cloud-box {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="cloud-glava">
            <h1>Психологическая помощь ВЫХОД ЕСТЬ!</h1>
            <img src="page_psih2.png" alt="Логотип компании">
        </div>
    </header>
    
    <nav>
        <a href="index.html">Главное</a> <a href="templates/reg_and_login.html">Услуги</a>
        
    </nav>
    
    <div class="info-container_1">
        <h2>О нас</h2>
        <p>Медицинский центр "Выход Есть!" – забота о вашем здоровье. Мы предлагаем широкий спектр медицинских услуг для вашего здоровья. У нас работают опытные специалисты в разных областях медицины. Мы гарантируем конфиденциальность и индивидуальный подход к каждому пациенту.</p>
        <p>Если вы ищете профессиональную медицинскую помощь, обратитесь в "Выход Есть!". Мы всегда готовы помочь вам быть здоровыми и счастливыми.</p>
    </div>
    
    <div class="cloud-container">
        <div class="cloud-box">
            <a href="trev.html"><h3>Тревога</h3></a> <!-- Исправлено: перенес ссылку на весь заголовок -->
        </div>
        <div class="cloud-box">
            <a href="depr.html"><h3>Депрессия/Антидепрессанты</h3></a>
        </div>
        <div class="cloud-box">
            <a href="zavi.html"><h3>Зависимость</h3></a>
        </div>
    </div>
    
    <footer>
        <img src="page_psih2.png" alt="Логотип компании">
        <pre>
ООО «Медико-диагностический центр «Выход Есть!» - это многопрофильное лечебно-профилактическое учреждение, которое имеет современную материально-техническую базу,
оказывает платные медицинские услуги и осуществляет консультации высококвалифицированных специалистов.
        </pre>
        <pre>
Обращаем ваше внимание на то, что данный интернет-сайт носит исключительно информационный характер и ни при каких условиях не является публичной офертой,
определяемой положениями ст. 405 Гражданского кодекса Республики Беларусь.
Для получения подробной информации о наличии и стоимости указанных услуг, пожалуйста, обращайтесь к администраторам клиники.
        </pre>
    </footer>
</body>
</html>
"""
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML-файл успешно создан!")

