from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def login(user: str, password: str):
    # 1. Configuramos las opciones para un servidor Linux sin pantalla
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Vuelve el navegador invisible
    chrome_options.add_argument("--no-sandbox")   # Requisito de seguridad para Linux
    chrome_options.add_argument("--disable-dev-shm-usage") # Evita caídas por falta de memoria
    
    # 2. Iniciamos el driver de Chrome (GitHub ya lo tiene instalado)
    driver = webdriver.Chrome(options=chrome_options)
    url_login = "https://sso.uc.cl/cas/login?service=https%3A%2F%2Fgo.ing.uc.cl%2Fforce"
    driver.get(url_login)

    time.sleep(3)

    campo_usuario = driver.find_element(By.XPATH, '//*[@id="username"]')
    campo_usuario.send_keys(user)

    campo_clave = driver.find_element(By.XPATH, '//*[@id="password"]')
    campo_clave.send_keys(password)
    campo_clave.send_keys(Keys.RETURN)
    time.sleep(2)
    print("logged in")
    return driver


def extraer_reservas(driver: webdriver):
    driver.get("https://go.ing.uc.cl/mis_reservas/")
    time.sleep(2)
    # Buscamos solo por la clase que identifica a las reservas
    cajas_reservas = driver.find_elements(By.CLASS_NAME, "request-item")
    lista_reservas = []

    for caja in cajas_reservas:
        texto_completo = caja.text
        if not texto_completo:
            continue
        
        lineas_texto = texto_completo.split("\n")
        fecha = None
        hora = None
        for linea in lineas_texto:
            if "calendar_today" in linea:
                # Quitamos la palabra 'calendar_today' y los espacios
                fecha = linea.replace("calendar_today", "").strip()
            elif "schedule" in linea:
                hora = linea.replace("schedule", "").strip()
        botones = caja.find_elements(By.TAG_NAME, "button")
        if len(botones) > 0:
            boton_info = botones[0]
            correo = boton_info.get_attribute("data-student-email")
            nombre = boton_info.get_attribute("data-student-name")
            descripcion = boton_info.get_attribute("data-student-description")
            curso = boton_info.get_attribute("data-course-name")

            reserva = {
                "curso": curso,
                "nombre": nombre,
                "correo": correo,
                "descripcion": descripcion,
                "fecha": fecha,
                "hora": hora
            }
            lista_reservas.append(reserva)
        print("conseguidas las reservas")
        for i in lista_reservas:
            print(i)
    return (lista_reservas)
