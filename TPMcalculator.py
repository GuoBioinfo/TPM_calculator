# import os
# cwd = os.getcwd()
# print(cwd)

# Open the ERCCsummary.csv file that contains the name, GenBank ID, concentration (attomole/µl)
# and length (nt) for each transcript. This file was created manually by extracting the information
# from file "SIRV_Set3_Norm_sequence-design-overview_20210507a.xlsx", Lexigon, Inc.
with open("ERCCsummary.csv") as ERCCsummary:
    ERCCinfo = ERCCsummary.readlines()
# print(samFilelines[1])

# Extract the concentration and length of each transcript.
erccConc = {}
erccLength = {}

for ERCC in ERCCinfo:
    erccConc[ERCC.split(",")[0]]=ERCC.split(",")[2].strip()
    erccLength[ERCC.split(",")[0]]=ERCC.split(",")[3].strip()
#print(erccLength)
#print(erccConc)

# Use the sam file to calculate the counts of sequencing reads aligned to each transcript.
# The sam file need to exclude the reads that are not aligned to the transcripts.
with open("ERCC.kapa.sam") as samFile:
    samFilelines = samFile.readlines()
# print(samFilelines[1])
transcriptsReadCount = {}
n=0
for samFileline in samFilelines:
    if samFileline[0] != "@":
        n += 1  # calcuate the total counts of sequencing reads aligned to the templates.
        # print(samFileline.split()[2])
        if samFileline.split()[2] in transcriptsReadCount.keys():
            transcriptsReadCount[samFileline.split()[2]] += 1
        else:
            transcriptsReadCount[samFileline.split()[2]] = 1
# print(transcriptsReadCount)
# print(n)
f = open("TranscriptReadCounts.csv", "w")
f.write("ERCC_ID, Read_count, Length(nt), Concentration(amoles/ul)"+"\n")
for key in transcriptsReadCount.keys():
    f.write(",".join([key,str(transcriptsReadCount[key]),erccLength[key],erccConc[key] + "\n"]))
f.write("Total reads: " + str(n))
f.close()
