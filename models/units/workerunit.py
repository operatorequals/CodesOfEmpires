from models.units import unit


class WorkerUnit(unit.Unit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.work_object = None
        self.work_rate = 0.1
        self.locals_['extract'] = self.extract
        self.locals_['collect'] = self.collect
        self.locals_['timber'] = self.timber


    def timber(self, work_object):
        self.work(work_object, 'wood')
    def collect(self, work_object):
        self.work(work_object, 'food')
    def extract(self, work_object):
        self.work(work_object, 'iron')


    def work(self, work_object, work_type):
        self.move(work_object.x, work_object.y)
        self.work_object = work_object
        self.work_type = work_type


    def update(self, td):
        super().update(td)
        if not self.work_object:
            return

        if not self.arrived(self.work_object.x, self.work_object.y):
            return

        r = self.work_object._collect(self.work_rate, self.work_type)
        self.team._stockpile(r, self.work_type)

