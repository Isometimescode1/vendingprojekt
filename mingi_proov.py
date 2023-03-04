kommi_olukord = []
kommi_olukord = [1 for i in range(6)]
print (kommi_olukord)



log = open("log_file.txt", "r")
kommi_olukord = list(log.read().splitlines())
print (kommi_olukord)

for lines , _ in enumerate(log):
    pass
lines += 1

for i in range(lines):
    kommi_olukord[i] = log.readline()
print (kommi_olukord)