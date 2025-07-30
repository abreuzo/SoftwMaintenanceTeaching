#Necessário para realizar import em python
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from controler.pedidoControler import PedidoControler
from controler.itemControler import ItemControler

class Janela3:
    def mostrar_janela3(database_name:str):
        print('----- CADASTRAR ITENS MENU ----------')
        q = int(input('Cadastrar novo item? (1-Sim/2-Não): '))
        if q==1:
            nome = str(input('Nome: ')).capitalize()
            preco = str(input('R$: ')).replace(',','.') #converte vírgula para ponto
            tipo = str(input('Tipo: (Bebida, Pizza, Hamburguer, etc): ')).capitalize()
            descricao = str(input('Descrição: ')).lower()

            preco = float(preco)#transforma preco par float #(manutenção) - corretiva - se não fizer a conversão de tipo apresenta erro

            item = ItemControler.create_item([nome,preco,tipo,descricao])#convertendo valores recebidos em um objeto do tipo item
            if item:
                insere_item = ItemControler.insert_into_item(database_name, item)
                if insere_item:
                    print('Item inserido com sucesso')
                else:
                    print('Erro ao inserir item')
        elif q==2:
            print('Retornando')
        else:
            print('Entrada inválida, retornando')