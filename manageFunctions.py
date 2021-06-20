#Basic coin functions
async def subCoin(user, subAmt):
    #Find the user's balance
    with open("userBal.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if "{0} = ".format(user) in line:
                content = line
                userBal = content[len(str(user)) + 3:]
                newBal = float(userBal) - float(subAmt)
                print("{0} = user new bal after sub".format(newBal))
    #Delete that line
    with open("userBal.txt", "w") as f:
        for line in lines:
            if str(user) not in line:
                f.write(line)
    #Re-write with updated balance
    with open("userBal.txt", "a") as userData:
        userData.write("\n{0} = {1}".format(user, float(newBal)))
    await cleanFile("userBal.txt")


#Add coins to a user
async def addCoin(user, addAmt):
    newBal = 0
    #Find the user's balance
    with open("userBal.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if "{0} = ".format(user) in line:
                print("Adding coins to {0}".format(user))
                content = line
                userBal = content[len(str(user)) + 3:]
                newBal = float(userBal) + float(addAmt)
                print("{0} = user new balance after add".format(newBal))
    #Delete that line
    with open("userBal.txt", "w") as f:
        for line in lines:
            if user not in line:
                f.write(line)
    #Re-write with updated balance
    with open("userBal.txt", "a") as userBal:
        userBal.write("\n{0} = {1}".format(user, newBal))
    await cleanFile("userBal.txt")


#Finding values
async def findVal(fileName, value):
    userData = open(fileName, 'r')
    for line in userData:
        if "{0}".format(value) in line:
            content = line
            val = content[len(str(value)) + 3:]
            return val


#Replace one value with another in a specified file
async def replaceVal(fileName, valueName, value):
    with open(fileName, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "{0} = ".format(valueName) in line:
                content = line
                userBal = content[len(str(valueName)) + 3:]
    #Delete that line
    with open(fileName, "w") as f:
        for line in lines:
            if valueName not in line:
                f.write(line)
    #Re-write with updated balance
    with open(fileName, "a") as userBal:
        userBal.write("\n{0} = {1}".format(valueName, value))
    #Remove any blank spaces
    await cleanFile(fileName)


#Removes blank spaces from files
async def cleanFile(filePath):
    data = open(filePath, "r").readlines()
    outFile = open(filePath, "w")
    for line in data:
        if not line.strip():
            continue
        outFile.write(line)

