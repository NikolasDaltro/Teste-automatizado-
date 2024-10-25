from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://teste2.ati.to.gov.br/login-unico-api-rel1/auth/login")

wait = WebDriverWait(driver, 20)  # 20 segundos de timeout

# Preenchendo os campos de login
username_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
username_field.send_keys("32.893.926/0001-40")

password_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
password_field.send_keys("123456")

login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginBtn"]')))
login_button.click()

# Aguardar a página carregar
driver.get("https://teste2.ati.to.gov.br/gestao-job-rel1/index.jsf")
time.sleep(2)

# Página Gestão de Job
driver.get("https://teste2.ati.to.gov.br/gestao-job-rel1/pagina/configuracao_job.jsf")
campo_nome = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="j_idt71:j_idt75"]')))
campo_nome.send_keys("Pedro Henique")
time.sleep(1)
campo_descri = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="j_idt71:j_idt78"]')))
campo_descri.send_keys("Fechar escalas")
time.sleep(1)
buscar = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_idt71:j_idt91"]/span[2]')))
buscar.click()

time.sleep(30)

# Página Monitoramento de Jobs
driver.get("https://teste2.ati.to.gov.br/gestao-job-rel1/pagina/monitorar_job.jsf")
time.sleep(5)

input("Pressione Enter para fechar o Chrome...")
driver.quit()
