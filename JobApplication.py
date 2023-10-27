class JobApplication:
    def __init__(self, company, job_title, submitted_date):
        self.submitted_date = submitted_date
        self.status = "active" # active, offer, or rejected
        self.company = company
        self.updates = [[submitted_date, "applied", "none"]]
    
    # Updates are going to be in the form of date,type,other information
    def add_update(self, update):
        self.updates.append(update)