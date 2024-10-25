from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Keys
from time import sleep

WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument("disable-infobars")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class TesteFront:
    def _init_(self, OPCOES, CAMPOS, FUNCOES):
        WINDOW_SIZE = "1920,1080"
        chrome_options = Options()
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.add_argument("disable-infobars")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(OPCOES["URL_SISTEMA"]+OPCOES["URI_TESTE"])
        self.tempoEsperaInicial = OPCOES["tempoEsperaInicial"]
        self.URL_SISTEMA = OPCOES["URL_SISTEMA"]
        self.URI_TESTE = OPCOES["URI_TESTE"]
        self.textoBase = OPCOES["textoBase"]
        self.campos = CAMPOS
        self.funcoes = FUNCOES
        self.logar(OPCOES["LOGIN"], OPCOES["SENHA"])
        
        self.resPesquisarAtivos = False
        self.resHistorico = False
        self.resCadastrar = False
        self.resCadastrarDup = False
        self.resBuscarRegistro = False
        self.resDesativar = False
        self.resConfirmarDesativar = False
        self.resAtivar = True
        self.resAlterar = False
        self.resExcluir = False
        self.resObrigatorios = False

        if self.funcoes["pesquisarAtivos"]:
            self.resPesquisarAtivos = self.pesquisarAtivos()
        if self.funcoes["historico"]:
            self.resHistorico = self.historico()
        if self.funcoes["cadastrar"]:
            self.resCadastrar = self.cadastrar()
        if self.funcoes["cadastrarDup"]:
            if not self.funcoes["cadastrar"]:
                self.resCadastrar = self.cadastrar()
            self.resCadastrarDup = self.cadastrarDup()
        if self.funcoes["buscarRegistro"]:
            if not self.funcoes["cadastrar"]:
                self.resCadastrar = self.cadastrar()
            self.resBuscarRegistro = self.buscarRegistro(self.textoBase)
        if self.funcoes["desativar"]:
            if not self.funcoes["cadastrar"]:
                self.resCadastrar = self.cadastrar()
            self.resDesativar = self.desativar()
            self.resAtivar = not self.resDesativar
        if self.funcoes["ativar"]:
            if not self.funcoes["cadastrar"]:
                self.resCadastrar = self.cadastrar()
            self.resAtivar = self.ativar()
        if self.funcoes["alterar"]:
            if not self.funcoes["cadastrar"]:
                self.resCadastrar = self.cadastrar()
            self.resAlterar = self.alterar()
        if self.funcoes["excluir"]:
            texto_busca = self.textoBase
            if not self.funcoes["cadastrar"]:
                self.resCadastrar = self.cadastrar()
            if self.resAlterar:
                texto_busca = self.textoBase + '_2'
            self.buscarRegistro(texto_busca)
            self.resExcluir = self.excluir()
        if self.funcoes["obrigatorios"]:
            obr_cad = self.resCadastrar
            texto_busca = self.textoBase
            if self.resAlterar:
                texto_busca = self.textoBase + '_2'
            if self.resExcluir:
                obr_cad = self.cadastrar()
                texto_busca = self.textoBase
            if not self.funcoes["cadastrar"]:
                obr_cad = self.cadastrar()
                texto_busca = self.textoBase
            self.camposObrigatoriosNaoPreenchidos(texto_busca)
            self.buscarRegistro(texto_busca)
            self.resExcluir = self.excluir()
        
    
    def _del_(self):
        self.driver.close()
    
    def logar(self, LOGIN, SENHA):
        current_url = self.driver.current_url
        if "login" in current_url:
            sleep(self.tempoEsperaInicial)
            campo_login = self.driver.find_element(By.XPATH,"//input[@id='username']")
            campo_login.send_keys(LOGIN)
            campo_senha = self.driver.find_element(By.XPATH,"//input[@id='password']")
            campo_senha.send_keys(SENHA)
            botao_logar = self.driver.find_element(By.XPATH,"//button[@class='btn login-button']")
            sleep(1)
            try:
                botao_logar.click()
                print(bcolors.OKGREEN + '[ + ] ' + bcolors.ENDC + 'Login OK!')
            except Exception as error:
                print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Erro ao Logar!')
                exit(0)
                
    def preencherCampo(self, campo, valor):
        if campo['tipo'] == 'text':
            input_text = self.driver.find_element(By.XPATH,"//input[@id='{}']".format(campo['nome']))
            input_text.clear()
            input_text.send_keys('{}'.format(valor))
        if campo['tipo'] == 'numero':
            input_number = self.driver.find_element(By.XPATH,"//input[@id='{}_input']".format(campo['nome']))
            valor = valor
            input_len = len(input_number.get_attribute("value"))
            for i in range(input_len):
                input_number.send_keys(Keys.BACKSPACE)
            input_number.send_keys('{}'.format(valor))
        if campo['tipo'] == 'select':
            input_select = self.driver.find_element(By.XPATH,"//div[@id='{}']".format(campo['nome']))
            input_select.click()
            sleep(1)
            input_option = self.driver.find_element(By.XPATH,"//li[@id='{}_{}']".format(campo['nome'], valor))
            input_option.click()

    def pesquisarAtivos(self):
        self.driver.get(self.URL_SISTEMA+self.URI_TESTE)
        sleep(1)
        try:
            input_select = self.driver.find_element(By.XPATH,"//div[contains(@aria-owns, ':j_')]")
            input_select.click()
            sleep(1)
            input_option = self.driver.find_element(By.XPATH,"//li[@data-label='Ativo']")
            input_option.click()
            botao_buscar = self.driver.find_element(By.XPATH,"//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-left btn-filtrar']")
            botao_buscar.click()
            sleep(1)
            print(bcolors.OKGREEN + '[ + ] ' + bcolors.ENDC + 'Buscar Ativos! OK')
            return True
        except Exception as error:
            print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Erro ao buscar ativos!')
            return False
    
    def historico(self):
        self.driver.get(self.URL_SISTEMA+self.URI_TESTE)
        sleep(2)
        try:
            botao_hist_geral = self.driver.find_element(By.XPATH,"//button[@title='Histórico Geral']")
            botao_hist_geral.click()
            print(bcolors.OKGREEN + '[ + ] ' + bcolors.ENDC + 'Acesso ao histórico geral! OK')
        except Exception as error:
            print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Erro ao verificar histórico Geral!')
            return False
        try:
            sleep(2)
            botao_hist_regs = self.driver.find_elements(By.XPATH,"//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only']")
            for botao_hist_reg in botao_hist_regs:
                botao_hist_reg.click()
                sleep(2)
                print(bcolors.OKGREEN + '[ + ] ' + bcolors.ENDC + 'Verificação de histórico de Registro! OK')
                break
            return True
        except Exception as error:
            print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Erro ao verificar histórico de Registro!')
            return False
    
    def cadastrar(self):
        self.driver.get(self.URL_SISTEMA+self.URI_TESTE)
        sleep(2)
        try:
            botao_cadastrar = self.driver.find_element(By.XPATH,"//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-left btn-controle']")
            botao_cadastrar.click()
            print(bcolors.OKGREEN + '[ + ] ' + bcolors.ENDC + 'Acessar o cadastro OK!') 
            sleep(2)
        except Exception as error:
            print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Erro ao acessar o cadastro!')
            return False
        for campo in self.campos:
            try:
                if campo['tipo'] == 'text':
                    input_text = self.driver.find_element(By.XPATH,"//input[@id='{}']".format(campo['nome']))
                    input_text.send_keys('{}'.format(campo['value']))
                if campo['tipo'] == 'numero':
                    input_number = self.driver.find_element(By.XPATH,"//input[@id='{}_input']".format(campo['nome']))
                    input_number.send_keys('{}'.format(campo['value']))
                if campo['tipo'] == 'select':
                    input_select = self.driver.find_element(By.XPATH,"//div[@id='{}']".format(campo['nome']))
                    input_select.click()
                    sleep(1)
                    input_option = self.driver.find_element(By.XPATH,"//li[@id='{}_{}']".format(campo['nome'], campo['value']))
                    input_option.click()
            except Exception as error:
                print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Erro ao preencher campos!')
                return False
        try:
            botao_salvar = self.driver.find_element(By.XPATH,"//button[@type='submit']")
            botao_salvar.click()
            sleep(1)
            print(bcolors.OKGREEN + '[ + ] ' + bcolors.ENDC + 'Cadastro! OK')
            return True
        except Exception as error:
            print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Erro ao salvar registro!')
            return False

    def cadastrarDup(self):
        self.driver.get(self.URL_SISTEMA+self.URI_TESTE)
        sleep(2)
        try:
            botao_cadastrar = self.driver.find_element(By.XPATH,"//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-left btn-controle']")
            botao_cadastrar.click()
            print(bcolors.OKGREEN + '[ + ] ' + bcolors.ENDC + 'Acessar o cadastro OK!') 
            sleep(2)
        except Exception as error:
            print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Erro ao acessar o cadastro!')
            return False
        for campo in self.campos:
            try:
                if campo['tipo'] == 'text':
                    input_text =self.driver.find_element(By.XPATH,"//input[@id='{}']".format(campo['nome']))
                    input_text.send_keys('{}'.format(campo['value']))
                if campo['tipo'] == 'numero':
                    input_number = self.driver.find_element(By.XPATH,"//input[@id='{}_input']".format(campo['nome']))
                    input_number.send_keys('{}'.format(campo['value']))
                if campo['tipo'] == 'select':
                    input_select = self.driver.find_element(By.XPATH,"//div[@id='{}']".format(campo['nome']))
                    input_select.click()
                    sleep(1)
                    input_option = self.driver.find_element(By.XPATH,"//li[@id='{}_{}']".format(campo['nome'], campo['value']))
                    input_option.click()
            except Exception as error:
                print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Erro ao preencher campos!')
                return False
        try:
            botao_salvar = self.driver.find_element(By.XPATH,"//button[@type='submit']")
            botao_salvar.click()
            sleep(2)
            resp = self.driver.find_element(By.XPATH,"//div[@class='ui-growl-item-container ui-state-highlight ui-corner-all ui-helper-hidden ui-shadow ui-growl-error']")
            if resp:
                print(bcolors.OKGREEN + '[ + ] ' + bcolors.ENDC + 'Verificação de duplicidade OK!')
                return True
            else:
                print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Falha ao verificar duplicidade!')    
                return False
        except Exception as error:
            print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Erro ao verificar duplicidade!')
            return False

    def buscarRegistro(self, registro):
        self.driver.get(self.URL_SISTEMA+self.URI_TESTE)
        sleep(2)
        try:
            input_text = self.driver.find_element(By.XPATH,"//input[@class='ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all filtro-input']")
            input_text.send_keys(registro)
            botao_buscar = self.driver.find_element(By.XPATH,"//button[@type='submit' and @aria-disabled='false']")
            botao_buscar.click()
            print(bcolors.OKGREEN + '[ + ] ' + bcolors.ENDC + 'Pesquisar! OK')
            sleep(2)
            return True
        except Exception as error:
            print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Erro ao pesquisar!')
            return False
    
    def desativar(self):
        try:
            botao_opcoes = self.driver.find_element(By.XPATH,"//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only']")
            botao_opcoes.click()
            sleep(1)
            if self.funcoes['confirmarDesativar']:
                botao_desativar = self.driver.find_element(By.XPATH,"//a[contains(@onclick, 'deactivate')]")
                botao_desativar.click() 
                sleep(1)
                input_motivo = self.driver.find_element(By.XPATH,"//textarea[contains(@id, 'motivo')]")
                input_motivo.send_keys(self.textoBase)
                botao_desativar_confirm = self.driver.find_element(By.XPATH,"//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only ui-button-success']")
                botao_desativar_confirm.click()
            else:
                botao_desativar = self.driver.find_element(By.XPATH,"//a[contains(@class, 'desativar')]")
                botao_desativar.click() 
            sleep(1)
            print(bcolors.OKGREEN + '[ + ]' + bcolors.ENDC + ' Desativar! OK')   
            sleep(1)
            return True
        except Exception as error:
            print(bcolors.FAIL + '[ - ]' + bcolors.ENDC + ' Erro ao Desativar!')
            return False

    def ativar(self):
        try:
            botao_opcoes = self.driver.find_element(By.XPATH,"//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only']")
            botao_opcoes.click()
            sleep(1)
            botao_ativar = self.driver.find_element(By.XPATH,"//a[contains(@onclick, ',p:')]")
            botao_ativar.click()
            print(bcolors.OKGREEN + '[ + ]' + bcolors.ENDC + ' Ativar! OK')   
            sleep(1)
            return True
        except Exception as error:
            print(bcolors.FAIL + '[ - ]' + bcolors.ENDC + ' Erro ao ativar!')
            return False
    
    def alterar(self):
        try:
            botao_opcoes = self.driver.find_element(By.XPATH,"//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only']")
            botao_opcoes.click()
            sleep(1)
            botao_alterar = self.driver.find_element(By.XPATH,"//a[contains(@href, 'cad.jsf?')]")
            botao_alterar.click()
            sleep(2)
            for campo in self.campos:
                try:
                    if campo['tipo'] == 'text':
                        input_text = self.driver.find_element(By.XPATH,"//input[@id='{}']".format(campo['nome']))
                        input_text.clear()
                        input_text.send_keys('{}_2'.format(campo['value']))
                    if campo['tipo'] == 'numero':
                        input_number = self.driver.find_element(By.XPATH,"//input[@id='{}_input']".format(campo['nome']))
                        valor = campo['value'] + 1
                        input_len = len(input_number.get_attribute("value"))
                        for i in range(input_len):
                            input_number.send_keys(Keys.BACKSPACE)
                        input_number.send_keys('{}'.format(valor))
                    if campo['tipo'] == 'select':
                        input_select = self.driver.find_element(By.XPATH,"//div[@id='{}']".format(campo['nome']))
                        input_select.click()
                        sleep(1)
                        input_option = self.driver.find_element(By.XPATH,"//li[@id='{}_{}']".format(campo['nome'], campo['value']))
                        input_option.click()
                except Exception as error:
                    print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Erro ao preencher campos!')
                    return False
            try:
                botao_salvar = self.driver.find_element(By.XPATH,"//button[@type='submit']")
                botao_salvar.click()
                sleep(2)
                resp = self.driver.find_element(By.XPATH,"//div[contains(@class,'ui-growl-info')]")
                if resp:
                    print(bcolors.OKGREEN + '[ + ] ' + bcolors.ENDC + ' Alterar OK!')
                    return True
                else:
                    print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + ' Erro ao alterar!')    
                    return False
            except Exception as error:
                print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + ' Erro ao alterar!')
                return False
        except Exception as error:
            print(bcolors.FAIL + '[ - ]' + bcolors.ENDC + ' Erro ao alterar!')
            return False
        
    def excluir(self):
        try:
            botao_opcoes = self.driver.find_element(By.XPATH,"//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only']")
            botao_opcoes.click()
            sleep(1)
            botao_excluir = self.driver.find_element(By.XPATH,"//a[@class='ui-menuitem-link ui-corner-all delete-action']")
            botao_excluir.click()
            sleep(1)
            botao_excluir_confirm = self.driver.find_element(By.XPATH,"//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-left ui-confirmdialog-yes']")
            botao_excluir_confirm.click()
            print(bcolors.OKGREEN + '[ + ]' + bcolors.ENDC + ' Excluir! OK')   
            sleep(1)
            return True
        except Exception as error:
            print(bcolors.FAIL + '[ - ]' + bcolors.ENDC + ' Erro ao Excluir!')
            return False
    
    def camposObrigatoriosNaoPreenchidos(self, texto_busca):
        for campo in self.campos:
            try:
                if campo['req']:
                    self.driver.get(self.URL_SISTEMA+self.URI_TESTE)
                    self.buscarRegistro(texto_busca)
                    botao_opcoes = self.driver.find_element(By.XPATH,"//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only']")
                    botao_opcoes.click()
                    sleep(1)
                    botao_alterar = self.driver.find_element(By.XPATH,"//a[contains(@href, 'cad.jsf?')]")
                    botao_alterar.click()
                    sleep(2)
                    try:
                        if campo['tipo'] == 'text':
                            input_text = self.driver.find_element(By.XPATH,"//input[@id='{}']".format(campo['nome']))
                            input_text.clear()
                        if campo['tipo'] == 'numero':
                            input_number = self.driver.find_element(By.XPATH,"//input[@id='{}_input']".format(campo['nome']))
                            input_len = len(input_number.get_attribute("value"))
                            for i in range(input_len):
                                input_number.send_keys(Keys.BACKSPACE)
                        if campo['tipo'] == 'select':
                            input_select = self.driver.find_element(By.XPATH,"//div[@id='{}']".format(campo['nome']))
                            input_select.click()
                            sleep(1)
                            input_option = self.driver.find_element(By.XPATH,"//li[@id='{}_0']".format(campo['nome']))
                            input_option.click()
                    except Exception as error:
                        print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + 'Erro ao preencher campos!')
                        return False
                    try:
                        botao_salvar = self.driver.find_element(By.XPATH,"//button[@type='submit']")
                        botao_salvar.click()
                        sleep(2)
                        resp = self.driver.find_element(By.XPATH,"//div[contains(@class,'ui-growl-error')]")
                        if resp:
                            print(bcolors.OKGREEN + '[ + ] ' + bcolors.ENDC + " Campo {} OK!".format(campo['nome']))
                        else:
                            print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + " Erro no campo {}".format(campo['nome']))    
                            return False
                    except Exception as error:
                        print(bcolors.FAIL + '[ - ] ' + bcolors.ENDC + ' Erro ao alterar!')
                        return False
            except Exception as error:
                print(bcolors.FAIL + '[ - ]' + bcolors.ENDC + ' Erro ao checar campos obrigatórios!')
                return False        
        print(bcolors.OKGREEN + '[ + ] ' + bcolors.ENDC + " Campos obrigatórios OK!")
        return True