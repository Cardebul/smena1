from ..models import AllWorkers

class MontPlan:

    def __init__(self, queryset, days, first_day):
        self.workers = [worker.pk for worker in queryset]
        self.days = days
        self.first_day = first_day
        self.hours = {worker: 144 for worker in self.workers}
        self.avg = len(self.workers) // 3
        self.table = {worker: [] for worker in self.workers}
    
    def calculate(self):
        all_monday = [i for i in range(1, self.days+1, 7)]
        all_sunday = [i for i in range(7, self.days+1, 7)]
        for _ in range(self.days):
            wk = sorted(self.hours, key=lambda x: self.hours[x], reverse=True)
            k = self.avg
            if self.first_day in all_monday:
                k += 1
            elif self.first_day in all_sunday:
                k -= 1
            smena = wk[:k]
            start = 1
            for i in self.table:
                if i in smena:
                    self.table[i].append(str(range(1,3)[start%2]))
                    start += 1
                    continue
                self.table[i].append('0')
            self.first_day += 1

            for i in range(k):
                self.hours[wk[i]] -= 12
        return
 

    def create_table(self):
        with open('table.txt', 'w') as t:
            for i in self.workers:
                t.write(str(i) + '  ')
                for j in self.table[i]:
                    t.write(str(j)+ '  ')
                t.write(str(144-self.hours[i]))
                t.write('\n')
        return
    
    def save_values(self, queryset, table):
        for i in queryset:
            allworkers = AllWorkers.objects.create(
                fio=i.fio,owner=i.owner,graphic = ''.join(self.table[i.pk]),table = table,cur_hours =  144 - self.hours[i.pk]
            )

            allworkers.save()

        return





def generate_graphic(queryset, table):
    import calendar
    month = table.date.month
    year = table.date.year
    days = calendar.monthrange(year, month)[1]
    first = calendar.weekday(year, month, 1) + 1
    
    qw = MontPlan(queryset, days, first)
    qw.calculate()
    qw.save_values(queryset, table)
    table.is_exists = True
    table.save()

