from pyspark import SparkContext
logFile = "file:////opt/modules/hadoop-2.8.5/README.txt"
sc = SparkContext("local", "first app")
logData = sc.textFile(logFile).cache()
numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()
print("Line with a:%i,lines with b :%i" % (numAs, numBs))