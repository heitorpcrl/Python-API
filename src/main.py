import csv

class Item:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {"nome": self.name, "preco": self.price, "quantidade": self.quantity}

class Inventory:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def show(self, gold):
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

class Store:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.items = self.load_items()

    def load_items(self):
        items = []
        with open(self.csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                items.append(Item(row["nome"], int(row["preco"]), int(row["quantidade"])))
        return items

    def save_items(self):
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fields = ["nome", "preco", "quantidade"]
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for item in self.items:
                writer.writerow(item.to_dict())

    def show_items(self):
        print("\nItens disponíveis na taberna:")
        for idx, item in enumerate(self.items):
            print(f"{idx+1}. {item.name} - {item.price} ouro (Estoque: {item.quantity})")

    def buy_item(self, inventory, gold):
        self.show_items()
        try:
            choice = int(input("Digite o número do item que deseja comprar: ")) - 1
        except ValueError:
            print("Opção inválida.")
            return
        if 0 <= choice < len(self.items):
            item = self.items[choice]
            if item.quantity <= 0:
                print("Item esgotado.")
            elif gold[0] >= item.price:
                inventory.add(Item(item.name, item.price, 1))
                gold[0] -= item.price
                item.quantity -= 1
                self.save_items()
                print(f"Você comprou {item.name}!")
            else:
                print("Ouro insuficiente.")
        else:
            print("Opção inválida.")

    def add_item(self):
        name = input("Digite o nome do item: ")
        try:
            price = int(input("Digite o preço do item: "))
            quantity = int(input("Digite a quantidade: "))
        except ValueError:
            print("Valor inválido.")
            return
        for item in self.items:
            if item.name.lower() == name.lower():
                item.quantity += quantity
                print(f"Quantidade de {item.name} aumentada para {item.quantity}.")
                self.save_items()
                return
        self.items.append(Item(name, price, quantity))
        self.save_items()
        print(f"Item {name} adicionado ao estoque.")

    def delete_item(self):
        self.show_items()
        try:
            choice = int(input("Digite o número do item que deseja deletar: ")) - 1
        except ValueError:
            print("Opção inválida.")
            return
        if 0 <= choice < len(self.items):
            removed = self.items.pop(choice)
            self.save_items()
            print(f"Item {removed.name} removido do estoque.")
        else:
            print("Opção inválida.")

class Admin:
    @staticmethod
    def request_password():
        password = input("Digite a senha de administrador: ")
        return password == "1234"

    @staticmethod
    def menu(store):
        if not Admin.request_password():
            print("Senha incorreta. Acesso negado.")
            return
        while True:
            print("\n--- Menu de Administração ---")
            print("1. Adicionar item ao estoque")
            print("2. Deletar item do estoque")
            print("3. Voltar ao menu principal")
            option = input("Escolha uma opção: ")
            if option == "1":
                store.add_item()
            elif option == "2":
                store.delete_item()
            elif option == "3":
                break
            else:
                print("Opção inválida.")

def main_menu():
    csv_path = "./items.csv"
    store = Store(csv_path)
    inventory = Inventory()
    gold = [50]
    while True:
        print("\nBem-vindo à Taberna do Aventureiro!")
        print("1. Ver itens à venda")
        print("2. Comprar item")
        print("3. Ver lista de itens")
        print("4. Administração")
        print("5. Sair")
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
            print("Volte sempre, aventureiro!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main_menu()