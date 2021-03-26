from models.units import unit

from resources import load

class WorkerUnit(unit.Unit):
    def __init__(self, *args, img=load.worker, **kwargs):
        super().__init__(*args, img=img, **kwargs)

        self.__working = False
        self.work_object = None
        self.work_rate = 0.1
        self.locals_['extract'] = self.extract
        self.locals_['collect'] = self.collect
        self.locals_['timber'] = self.timber
        self.locals_['finished'] = self.finished
        self.locals_['stop_work'] = self.stop_work

    def timber(self, work_object):
        self.work(work_object, 'wood')
    def collect(self, work_object):
        self.work(work_object, 'food')
    def extract(self, work_object):
        self.work(work_object, 'iron')


    def work(self, work_object, work_type):
        self.stop()
        self.work_object = work_object
        self.move(work_object.x, work_object.y)
        self.work_type = work_type


    def stop_work(self):
        self.work_object = None
        self.__working = True
        self.work_type = None


    def finished(self):
        return self.work_object is None


    def update(self, td):
        super().update(td)
        if not self.work_object:
            return

        if not self.arrived(
                    (self.work_object.x, self.work_object.y)
                ):
#            print(f"Stopped working as it is away - {self.__working}")
            if self.__working:
                self.stop_work()
            return

#        print(self.x, self.y, "->", self.work_object.x, self.work_object.y)
        r = self.work_object._collect(self.work_rate, self.work_type)
        self.__working = True
        if r <= 0:
            self.stop_work()
            return
        self.team._stockpile(r, self.work_type)

