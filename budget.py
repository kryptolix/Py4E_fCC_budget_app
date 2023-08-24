class Category():
  def __init__(self, name):
    self.name = name
    self.ledger = []
    self.ledger_wd = []

  def __str__(self):
    string = self.name.center(30, "*") + "\n"
    for line in self.ledger:
      if len(line["description"]) > 24:
        string += line["description"][:23] + f'{line["amount"]:7.2f}' + "\n"
      else:
        string += f'{line["description"]: <23}{line["amount"]:7.2f}' + "\n" 
    string += f'Total: {self.get_balance()}'
    return string
    
  def get_balance(self):
    balance = 0
    for line in self.ledger:
      balance += line["amount"]
    return balance

  def check_funds(self, amount):
    if self.get_balance() >= amount:
      return True
    else:
      return False
    
  def deposit(self, amount, description = ""):
    self.ledger.append({"amount": float(amount), "description": description})

  def withdraw(self, amount, description = ""):
    if self.check_funds(float(amount)) == True:
      self.ledger.append({"amount": -amount, "description": description})
      self.ledger_wd.append(amount)
      return True
    else:
      return False

  def transfer(self, amount, other_category):
    if self.check_funds(amount) == True:
      self.withdraw(amount, f"Transfer to {other_category.name}")
      other_category.deposit(amount, f"Transfer from {self.name}")
      return True
    else:
      return False

def create_spend_chart(categories):
  chart = "Percentage spent by category\n"
  percent_list = list()
  total_spent = 0
  stage = 100

# Calculate total withdrawals
  for cat in categories:
    total_spent += float(sum(cat.ledger_wd))

# Calculate Percent values
  for cat in categories:
    percent_list.append({"percent": int(sum(cat.ledger_wd) / total_spent * 10)*10, "name" : cat.name})

# Generate diagram
  while stage >= 0:    
    chart += (f"{stage: >3}| ")
    for line in percent_list:
      if line['percent'] >= stage:
        chart += f"o  "
      else:
        chart += f"   "
    chart += "\n"
    stage -= 10
# Generate X-axis
  chart += "    " + len(percent_list) * "---" + "-\n"
# Write names vertically under X-axis
  maxLen = 0
  for item in percent_list:
    length = len(item["name"])
    if length > maxLen:
      maxLen = length
  for item in percent_list:
    item["name"] = item["name"].ljust(maxLen)
  for i in range(maxLen):
    chart += "     "
    for item in percent_list:
      chart += item["name"][i] + "  "
    if i < maxLen - 1:
      chart += "\n"
  print(chart)
  return chart