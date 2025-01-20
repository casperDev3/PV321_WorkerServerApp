from django_cron import CronJobBase, Schedule

class NotificationCron(CronJobBase):
    schedule = Schedule(run_every_mins=1/60) # every 1 second
    code = 'Notifications.cron.NotificationCron'

    def do(self):
        print("____Hello, world!")
        pass