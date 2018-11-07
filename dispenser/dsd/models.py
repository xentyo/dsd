class Metric:
    def __init__(self, *args, **kwargs):
        self.symbol = kwargs.get('symbol')
        self.name = kwargs.get('name')


class Product:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')


class Kit(Product):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = kwargs.get('products')


class Inventory:
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.product = kwargs.get('product')
        self.metric = kwargs.get('metric')
        self.quantity = kwargs.get('quantity')

    def sold(self, quantity):
        if quantity > self.quantity:
            raise Exception('quantity to sold excedes inventory quantity')
        self.quantity = self.quantity - quantity

    def supply(self, quantity):
        self.quantity = self.quantity + quantity


class Dispenser:
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.inventories = []
        if kwargs.get('inventories') is not None:
            self.inventories = kwargs.get('inventories')

    def dispense(self, **kwargs):
        inventory = kwargs.get('inventory')
        quantity = kwargs.get('quantity')
        if isinstance(inventory, 'Inventory'):
            inventory = self.getInventory(inventory.id)
        else:
            inventory = self.getInventory(inventory)
        if inventory:
            inventory.sold(quantity)

    def getInventory(self, id):
        for i in self.inventories:
            if i.id == id:
                return i
        return None
    
    def addInventory(self, inventory):
        return self.inventories.append(inventory)
