#para pegar a data de hoje
from datetime import date
import time

#Necessário para realizar import em python
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

#importando os módulos de model
from model.pedido import Pedido

#importando os módulos de controle
from controler.pedidoControler import PedidoControler
from controler.itemControler import ItemControler

#criação da classe janela
class Janela1:
    
    @staticmethod
    def mostrar_janela1(database_name: str) -> None:
        """
        View para o usuário utilizar o software
        
        return None
        """
        
        a = 'y'
        
        menu = ItemControler.mostrar_itens_menu(database_name)
        #(manutenção) - adptativa -> melhora o menu visualmente
        exibir_menu=''
        for elem in menu:
            exibir_menu+=f'Id: {elem[0]}|| Tipo: {elem[2]}|| Sabor: {elem[1]}|| Descricao: {elem[4]}|| R$ {elem[2]}\n'
        
        print('----------Menu----------\n')
        print(f'{exibir_menu}\n')
        # print(f'{menu} \n') //deixar dessa forma para os alunos
        while a=='y':
            lista_itens = []
            valor_total=0
            #bug1 - e se o usuário estiver com o caixa alta ligada? 
            a = str(input('Cadastrar pedido (y-Sim, n-Nao): ')).lower() #(manutenção) - corretiva -> padroniza entrada de dados para seleção
            
            if a=='y':
                print('----------Cadastrar pedido----------\n')
                adicionar = 'y'
                pedidos = PedidoControler.search_in_pedidos_all(database_name)
                numero_pedido = len(pedidos)+1
                while adicionar == 'y':
                    item = int(input('Numero do item: '))
                    quantidade = int(input('Quantidade: '))
                    
                    #calculando em tempo de execução o valor do pedido
                    a = ItemControler.valor_item(database_name, item)
                    b = a[0][0]*quantidade
                    print(b)
                    valor_total+=b
                    
                    for x in range(0,quantidade):#acrescentado o mesmo item várias vezes, de acordo com a quantidade
                        lista_itens.append((numero_pedido,item))
                    #bug2 - e se o usuário estiver com o caixa alta ligada? 
                    adicionar = str(input('Adicionar novo item? (y-Sim, n-Nao): ')).lower()#(manutenção) - corretiva -> padroniza entrada de dados para seleção
                
                print('\n----------Finalizar pedido----------\n')
                print(f'Numero do pedido: {numero_pedido}')
                delivery = str(input('Delivery (S/N): ')).lower()
                if delivery=='s':
                    delivery = True
                elif delivery=='n':
                    delivery = False
                else:
                    print('Valor incorreto, recomeçando')
                    break
                endereco = str(input('Endereco:'))
                # if isinstance(endereco, (tuple, list)):
                #     endereco = 'Não informado'
                status_aux = int(input('status: 1-preparo, 2-pronto, 3-entregue: '))
                
                
                
                #bug 3 - se digtar qualquer número inteiro diferente de 1 ou 2 ele já assume status = entregue
                #bug 4 - quando status_aux = 1 ele não computa, pois, o if e else do final trabalham juntos
                if status_aux == 1:
                    status = 'preparo'
                elif status_aux == 2: #(manutenção) - corretiva -> (elif, para uma checagem de 3 casos, if, elif e else)
                    status = 'pronto'
                elif status_aux == 3: #(manutenção) - corretiva -> (especificando o terceiro caso, para apenas quando 3 for digitado status ser entregue)
                    status = 'entregue'
                else:
                    print('Entrada inválida - pedido cancelado')
                    break
 
                print(f'Valor Final: R${valor_total}')
                data_hoje = date.today()
                data_formatada = data_hoje.strftime('%d/%m/%Y')
                print(data_formatada)
                print(endereco)
                pedido = Pedido(status, str(delivery), endereco,data_formatada,float(valor_total))
                PedidoControler.insert_into_pedidos(database_name,pedido)
                for elem in lista_itens:
                    ItemControler.insert_into_itens_pedidos(database_name,elem)
                
            elif a=='n': #(manutenção) - corretiva (elif ao invés de if)
                print('Voltando ao Menu inicial')
                time.sleep(2)
                break
                
            else: #(manutenção) - corretiva (acrescentado para checar qualquer coisa diferente de y ou n)
                print('Entrada inválida')
                
#---------------MANUTENÇÕES---------------#
#corretiva - para cadastrar pedido, se o usuário digitar qualquer coisa diferente
#de y ou n não irá fazer nada o código

#corretiva - se o usuário estiver com o caps lock ligado e digitar em maiúsculo,
#ainda que as opções corretas, não irá reconhecer

#corretiva - ao checar o status de um pedido, o primeiro status nunca é computado