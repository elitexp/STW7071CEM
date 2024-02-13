from crontab import CronTab
print("CRONing the scheduler")
cron = CronTab(user=True)
job = cron.new(command=f'python {__file__}')
job.setall('0 0 * * 0')  # Run at midnight (00:00) every Sunday (0)
cron.write()
print("Successfully CRONned the scheduler job")
