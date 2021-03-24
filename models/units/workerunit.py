from models.units import unit

from resources import load

class WorkerUnit(unit.Unit):
    def __init__(self, *args, img=load.worker, **kwargs):
        super().__init__(*args, img=img, **kwargs)

        self.work_object = None
        self.work_rate = 1
        self.locals_['extract'] = self.extract
        self.locals_['collect'] = self.collect
        self.locals_['timber'] = self.timber
        self.locals_['finished'] = self.finished


    def timber(self, work_object):
        self.work(work_object, 'wood')
    def collect(self, work_object):
        self.work(work_object, 'food')
    def extract(self, work_object):
        self.work(work_object, 'iron')


    def work(self, work_object, work_type):
        self.work_object = work_object
        self.move(work_object.x, work_object.y)
        self.work_type = work_type


    def _stop(self):
        self.work_object = None


    def finished(self):
        return self.work_object is None


    def update(self, td):
        super().update(td)
        if not self.work_object:
            return
        if not self.arrived((self.work_object.x, self.work_object.y)):
            return

        r = self.work_object._collect(self.work_rate, self.work_type)
        if r <= 0:
            self.work_object = None
            return
        self.team._stockpile(r, self.work_type)

