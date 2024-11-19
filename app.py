from fastapi import FastAPI, Body
from datetime import datetime

def complete_order():
    return [upd for upd in repo if upd.status == "completed"]
#Сущность
class Order:
    def __init__(self, number, day, month, year, device, problem_type, description, client, status,):
        self.number = number
        self.startDate = datetime(day, month, year)
        self.endDate = None
        self.device = device
        self.problem_type = problem_type
        self.description = description
        self.client = client
        self.status = status
        self.master = "not assigned"
        self.comments = []

order = Order(1, 18,11,2024, "iphone", "window", "1", "Vasya", "completed", "Oleg")

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
                if(order.status == "completed"):
                    order.endDate == datetime.now()
        if(order.status != dto["status"]):
            order.status = dto["status"]
        if(order.description != dto["description"]):
            order.description = dto["description"]
        if(order.master != dto["master"]):
            order.master = dto["master"]
        if(dto["comments"] != None):
            order.comments.append(dto["comments"])
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

#количество всех выполненых заявок.
@app.get("/completeCounts")
def complete_counts():
    return len(complete_order())

#Статистика по типам не исправностей.
@app.get("/problemTypes")
def problem_types():
    result = {}
    for upd in repo:
        if upd.problem_type in result:
            result[upd.problem_type] += 1
        else:
            result[upd.problem_type] = 1
    return result


#Среднее выполнение заявки.
@app.get("/average")
def average():
    completed = complete_counts()
    times = []
    for upd in completed:
        times.append(upd.endDate - upd.startDate)
    time_sum = sum([t.days for t in times]) #время завершение каждой заявки. В днях. В сумме сколько дней выполнялась заявка.
    ord_count = complete_counts() #количество выполненных заявок.
    result = time_sum / ord_count
    return result