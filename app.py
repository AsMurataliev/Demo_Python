from fastapi import FastAPI
 
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
def create_order(order = Order):
    repo.append(order)
    return repo
    
