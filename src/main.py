#Nomes: Heitor Santos Cortes e Felipe Shinkae.
#Professor: Richard
#Matéria: Programação Orientada a objetos.

import csv
from typing import List, Dict
from config import *
from logger import logger
from exceptions import *

logger.debug("Esta é uma mensagem de debug")
logger.info("Esta é uma mensagem de informação")
logger.warning("Esta é uma mensagem de aviso")
logger.error("Esta é uma mensagem de erro")
logger.critical("Esta é uma mensagem crítica")

class Item:
    
    def __init__(self, name: str, price: int, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity
        logger.info(f"Item criado: {name}")

    def to_dict(self) -> Dict[str, any]:
        return {"nome": self.name, "preco": self.price, "quantidade": self.quantity}

class Inventory:
    
    def __init__(self):
        self.items: List[Item] = []
        logger.info("Inventário criado")

    def add(self, item: Item) -> None:
        self.items.append(item)
        logger.info(f"Item adicionado ao inventário: {item.name}")

    def show(self, gold: List[int]) -> None:
        print("\nSeu inventário:")
        total = 0
        if self.items:
            for item in self.items:
                print(f"- {item.name} ({item.price} ouro)")
                total += item.price
            print(f"Valor total gasto: {total} ouro")
        else:
            print("Inventário vazio.")
        print(f"Ouro restante: {gold[0]}")
        logger.info(f"Inventário exibido. Total gasto: {total} ouro")

class Store:
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.items: List[Item] = self.load_items()
        logger.info("Loja inicializada")

    def load_items(self) -> List[Item]:
        items = []
        try:
            with open(self.csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    items.append(Item(row["nome"], int(row["preco"]), int(row["quantidade"])))
            logger.info(f"Carregados {len(items)} itens do arquivo CSV")
        except FileNotFoundError:
            logger.error(f"Arquivo {self.csv_path} não encontrado")
            raise
        return items

    def save_items(self) -> None:
        try:
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fields = ["nome", "preco", "quantidade"]
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                for item in self.items:
                    writer.writerow(item.to_dict())
            logger.info("Itens salvos no arquivo CSV")
        except Exception as e:
            logger.error(f"Erro ao salvar itens: {str(e)}")
            raise

    def show_items(self) -> None:
        
        print("\nItens disponíveis na taberna:")
        for idx, item in enumerate(self.items, 1):
            print(f"{idx}. {item.name} - {item.price} ouro (Estoque: {item.quantity})")
        logger.info("Lista de itens exibida")

    def buy_item(self, inventory: Inventory, gold: List[int]) -> None:
        self.show_items()
        try:
            choice = int(input("Digite o número do item que deseja comprar: ")) - 1
        except ValueError:
            logger.warning("Tentativa de compra com opção inválida")
            raise InvalidOptionError(MESSAGES["invalid_option"])

        if not 0 <= choice < len(self.items):
            logger.warning(f"Tentativa de compra com índice inválido: {choice}")
            raise InvalidOptionError(MESSAGES["invalid_option"])

        item = self.items[choice]
        if item.quantity <= 0:
            logger.warning(f"Tentativa de compra de item esgotado: {item.name}")
            raise ItemSoldOutError(MESSAGES["item_sold_out"])
        
        if gold[0] < item.price:
            logger.warning(f"Tentativa de compra sem ouro suficiente: {gold[0]} < {item.price}")
            raise InsufficientGoldError(MESSAGES["insufficient_gold"])

        inventory.add(Item(item.name, item.price, 1))
        gold[0] -= item.price
        item.quantity -= 1
        self.save_items()
        print(f"Você comprou {item.name}!")
        logger.info(f"Item comprado: {item.name}")

    def add_item(self) -> None:
        name = input("Digite o nome do item: ")
        try:
            price = int(input("Digite o preço do item: "))
            quantity = int(input("Digite a quantidade: "))
        except ValueError:
            logger.warning("Tentativa de adicionar item com valores inválidos")
            raise InvalidOptionError("Valor inválido.")

        for item in self.items:
            if item.name.lower() == name.lower():
                item.quantity += quantity
                print(f"Quantidade de {item.name} aumentada para {item.quantity}.")
                self.save_items()
                logger.info(f"Quantidade do item {item.name} atualizada para {item.quantity}")
                return

        self.items.append(Item(name, price, quantity))
        self.save_items()
        print(f"Item {name} adicionado ao estoque.")
        logger.info(f"Novo item adicionado: {name}")

    def delete_item(self) -> None:
        self.show_items()
        try:
            choice = int(input("Digite o número do item que deseja deletar: ")) - 1
        except ValueError:
            logger.warning("Tentativa de deletar item com opção inválida")
            raise InvalidOptionError(MESSAGES["invalid_option"])

        if not 0 <= choice < len(self.items):
            logger.warning(f"Tentativa de deletar item com índice inválido: {choice}")
            raise InvalidOptionError(MESSAGES["invalid_option"])

        removed = self.items.pop(choice)
        self.save_items()
        print(f"Item {removed.name} removido do estoque.")
        logger.info(f"Item removido: {removed.name}")

class Admin:
    @staticmethod
    def request_password() -> bool:
        password = input("Digite a senha de administrador: ")
        is_valid = password == ADMIN_PASSWORD
        if not is_valid:
            logger.warning("Tentativa de acesso administrativo com senha incorreta")
        return is_valid

    @staticmethod
    def menu(store: Store) -> None:
        if not Admin.request_password():
            logger.warning("Acesso administrativo negado")
            raise AuthenticationError(MESSAGES["wrong_password"])

        while True:
            print("\n--- Menu de Administração ---")
            for key, value in ADMIN_MENU_OPTIONS.items():
                print(f"{key}. {value}")
            
            option = input("Escolha uma opção: ")
            if option == "1":
                store.add_item()
            elif option == "2":
                store.delete_item()
            elif option == "3":
                break
            else:
                logger.warning(f"Opção administrativa inválida: {option}")
                print(MESSAGES["invalid_option"])

def main_menu() -> None:
    store = Store(CSV_PATH)
    inventory = Inventory()
    gold = [INITIAL_GOLD]
    logger.info("Sistema iniciado")

    while True:
        print(f"\n{MESSAGES['welcome']}")
        for key, value in MAIN_MENU_OPTIONS.items():
            print(f"{key}. {value}")
        
        try:
            option = input("Escolha uma opção: ")
            if option == "1":
                store.show_items()
            elif option == "2":
                store.buy_item(inventory, gold)
            elif option == "3":
                inventory.show(gold)
            elif option == "4":
                Admin.menu(store)
            elif option == "5":
                print(MESSAGES["goodbye"])
                logger.info("Sistema encerrado")
                break
            else:
                logger.warning(f"Opção inválida selecionada: {option}")
                print(MESSAGES["invalid_option"])
        except TabernaError as e:
            print(str(e))
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            print("Ocorreu um erro inesperado. Por favor, tente novamente.")

if __name__ == "__main__":
    main_menu()