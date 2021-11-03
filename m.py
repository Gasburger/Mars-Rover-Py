import mosspy

userid = 987654321

m = mosspy.Moss(userid, "python")

#m.addBaseFile("client.py")
m.addBaseFile("client_RH.py")

# Submission Files
m.addFile("client.py")

url = m.send() # Submission Report URL

print ("Report Url: " + url)

# Save report file
m.saveWebPage(url, "report.html")

# Download whole report locally including code diff links
mosspy.download_report(url, "report/", connections=8)