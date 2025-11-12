import time
def countdown(start, step, alert_every = 5):
    counter = 0
    while start >= 0:
        print(start)
        if counter >= alert_every:
            print(f"{start} seconds left")
            counter = 0
        time.sleep(0.5)
        start -= 1
        counter += step
    print("Time’s up!")
start_time = int(input("enter the start time"))
# step_s = float(input("enter the step (default 0.5)")or 0.5)
alert_interval = float(input("enter the alert interval (default 5)")or 5)
countdown(start_time,0.5, alert_interval)


