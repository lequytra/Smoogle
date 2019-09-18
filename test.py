import validators

t = "#ViewPollResults"
if validators.url(t):
    print("success")
else:
    print("no")