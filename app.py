from fastapi import FastAPI, Body
 
class Order:
    def __init__(self, number, day, month, year, device, problem_type, description, client, status):
        self.number = number
        self.day = day
        self.month = month
        self.year = year
        self.device = device
        self.problem_type = problem_type
        self.description = description
        self.client = client
        self.status = status

order = Order(1, 18,11,2024, "iphone", "window", "1", "Vasya", "not ready")

repo = []
repo.append(order)

app = FastAPI()
@app.get("/")
def read_root():
    return repo


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
        data["status"]
    )
    repo.append(order)
    return order

@app.put("/{number}")
def update_order(number, dto = Body()):
    isEmpty = True
    for order in repo:
        if order.number == int(number):
            isEmpty= False
            order.status = dto["status"]
            order.description = dto["description"]
            order.master = dto["master"]
            return order
    if isEmpty:
        return "Order not found"