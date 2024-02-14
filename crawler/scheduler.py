from crontab import CronTab
import os
print("CRONing the scheduler")
cron = CronTab(user=True)
job = cron.new(command=f'python {os.path.dirname(__file__)}/crawl.py')
job.setall('0 0 * * 0')  # Run at midnight (00:00) every Sunday (0)
cron.write()
print("Successfully CRONned the scheduler job")
