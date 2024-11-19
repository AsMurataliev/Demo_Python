from fastapi import FastAPI, Body
 
#Сущность
class Order:
    def __init__(self, number, day, month, year, device, problem_type, description, client, status,master):
        self.number = number
        self.day = day
        self.month = month
        self.year = year
        self.device = device
        self.problem_type = problem_type
        self.description = description
        self.client = client
        self.status = status
        self.master = "not assigned"

order = Order(1, 18,11,2024, "iphone", "window", "1", "Vasya", "not ready", "Oleg")

#Уведомление об изменении статуса заказа.
isUpdatedStatus = False
message = ""
isEmpty = True

repo = []
repo.append(order)

app = FastAPI()

#Получвение всех заказов.
@app.get("/")
def read_root():
    global isUpdatedStatus
    global message
    if(isUpdatedStatus):
        upd = message
        isUpdatedStatus = False
        message= ""
        return repo, upd
    else:
        return repo

#Добавление нового заказа.
@app.post("/")
def create_order(data = Body()):
    order = Order(
        data["number"],
        data["day"],
        data["month"],
        data["year"],
        data["device"],
        data["problem_type"],
        data["description"],
        data["client"],
        data["status"],
        data["master"]
    )
    repo.append(order)
    return order

#Изменение заказа по номеру
@app.put("/{number}")
def update_order(number, dto = Body()):
    global isUpdatedStatus
    global message
    global isEmpty
    for order in repo:
        if order.number == int(number):
            isEmpty= False
            if(order.status != dto["status"]):
                isUpdatedStatus= True
                message += "Order status number " + str(order.number) + " changed"
        if(order.status != dto["status"]):
            order.status = dto["status"]
        if(order.description != dto["description"]):
            order.description = dto["description"]
        if(order.master != dto["master"]):
            order.master = dto["master"]
        return order
    if isEmpty:
        return "Order not found"
    
#Получение заказов по номеру.
@app.get("/number/{number}")
def get_by_number(number):
    for order in repo:
        if order.number == int(number):
            return order
    return "Order not found"

#Получение 
@app.get("/filter/{param}")
def get_by_param(param):
    return [upd for upd in repo if upd.device == param or upd.problem_type == param or upd.description == param or upd.client == param or upd.status == param or upd.master == param]
