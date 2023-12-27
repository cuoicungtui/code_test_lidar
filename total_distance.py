import serial
from CalcLidarData import CalcLidarData

ser = serial.Serial(port='/dev/tty.usbserial-0001',
                    baudrate=230400,
                    timeout=5.0,
                    bytesize=8,
                    parity='N',
                    stopbits=1)

tmpString = ""
total_distance = 0

i = 0
while True:
    loopFlag = True
    flag2c = False

    while loopFlag:
        b = ser.read()
        tmpInt = int.from_bytes(b, 'big')

        if tmpInt == 0x54:
            tmpString += b.hex() + " "
            flag2c = True
            continue

        elif tmpInt == 0x2c and flag2c:
            tmpString += b.hex()

            if not len(tmpString[0:-5].replace(' ', '')) == 90:
                tmpString = ""
                loopFlag = False
                flag2c = False
                continue

            lidarData = CalcLidarData(tmpString[0:-5])

            # Summing up the distances
            total_distance += sum(lidarData.Distance_i)

            tmpString = ""
            loopFlag = False

        else:
            tmpString += b.hex() + " "

        flag2c = False

    i += 1
    print(f"Total Distance: {total_distance} units")  # Output total distance
