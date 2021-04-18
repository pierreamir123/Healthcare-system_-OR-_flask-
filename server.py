from flask import Flask, render_template, request, redirect, url_for, session, flash
from calender import sync_cal
import mysql.connector 
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "mysql"
)
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS ORDep")
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "mysql",
    database = "ORDep"
)
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS Doctors (UserName VARCHAR(255), ID INT, PassWord VARCHAR(20), FirstName VARCHAR(255), LastName VARCHAR(255),Gender VARCHAR(10) ,Nationality VARCHAR(255),BDay INT,BMonth INT,BYear INT, Mobile INT ,Email VARCHAR(255),Address VARCHAR(255),PRIMARY KEY(ID), image blob)")
mycursor.execute("CREATE TABLE IF NOT EXISTS Admins (UserName VARCHAR(255), ID INT, PassWord VARCHAR(20),FirstName VARCHAR(255), LastName VARCHAR(255),Gender VARCHAR(10) ,Nationality VARCHAR(255),BDay INT,BMonth INT,BYear INT,Mobile INT, Email VARCHAR(255),Address VARCHAR(255),PRIMARY KEY(ID), image blob)")
mycursor.execute("CREATE TABLE IF NOT EXISTS Patients (UserName VARCHAR(255), ID INT, PassWord VARCHAR(20),FirstName VARCHAR(255), LastName VARCHAR(255),Gender VARCHAR(10) ,Nationality VARCHAR(255),BDay INT,BMonth INT,BYear INT,Mobile INT,Email VARCHAR(255),Address VARCHAR(255), Weight INT, Height INT, ChronicDiseases VARCHAR(255), Allergies VARCHAR(255), PreviousOperations VARCHAR(255),PRIMARY KEY(ID), image blob)")
mycursor.execute("CREATE TABLE IF NOT EXISTS OperationRooms ( RoomNumber INT, PRIMARY KEY(RoomNumber) )")
mycursor.execute("CREATE TABLE IF NOT EXISTS Operations ( ID INT, PRIMARY KEY(ID), Type VARCHAR(100), Day INT, Month INT, Year INT, OperationLevel VARCHAR(20), EstimatedHours INT, PatientID INT, FOREIGN KEY (PatientID) REFERENCES Patients(ID), LeadingDoctorID INT, FOREIGN KEY (LeadingDoctorID) REFERENCES Doctors(ID), Status VARCHAR(25))")
mycursor.execute("CREATE TABLE IF NOT EXISTS ConfirmedOperations ( OperationID INT, FOREIGN KEY (OperationID) REFERENCES Operations(ID), StartTime INT, EstimatedEndTime INT, OperationRoomNumber INT , FOREIGN KEY (OperationRoomNumber) REFERENCES OperationRooms(RoomNumber), EndingStatus VARCHAR(25), TableInsertionOrder INT AUTO_INCREMENT, PRIMARY KEY (TableInsertionOrder))")
mycursor.execute("CREATE TABLE IF NOT EXISTS CancelledOperations (OperationID INT, FOREIGN KEY (OperationID) REFERENCES Operations(ID) ,  StartTime INT, EstimatedEndTime INT, OperationRoomNumber INT , FOREIGN KEY (OperationRoomNumber) REFERENCES OperationRooms(RoomNumber) )")
mycursor.execute("CREATE TABLE IF NOT EXISTS AssistingDoctors ( OperationID INT, FOREIGN KEY (OperationID) REFERENCES Operations(ID), DoctorID INT, FOREIGN KEY (DoctorID) REFERENCES Doctors(ID) )")

#Server

app = Flask(__name__)
app.secret_key = "abc"

@app.route('/')
def HomePage():
    return render_template("HomePage.html")

@app.route('/ReservationRequestFormPage', methods=['GET', 'POST'])
def ReservationRequestFormPage():
    if request.method == "POST" :

        OperationType = request.form['OperationType']
        LeadingDoctorID = request.form['LeadingDoctorID']
        OperationDay = request.form['OperationDay']
        OperationMonth = request.form['OperationMonth']
        OperationYear = request.form['OperationYear']
        OperationLevel = request.form['OperationLevel']
        EstimatedHours = request.form['EstimatedHours']
        PatientFirstName = request.form['PatientFirstName']
        PatientLastName = request.form['PatientLastName']

        AssistingDoc1FirstName = request.form['AssistingDoc1FirstName']
        AssistingDoc1LastName  = request.form['AssistingDoc1LastName']
        AssistingDoc2FirstName = request.form['AssistingDoc2FirstName']
        AssistingDoc2LastName  = request.form['AssistingDoc2LastName']
        AssistingDoc3FirstName = request.form['AssistingDoc3FirstName']
        AssistingDoc3LastName  = request.form['AssistingDoc3LastName']
        AssistingDoc4FirstName = request.form['AssistingDoc4FirstName']
        AssistingDoc4LastName  = request.form['AssistingDoc4LastName']
        AssistingDoc5FirstName = request.form['AssistingDoc5FirstName']
        AssistingDoc5LastName  = request.form['AssistingDoc5LastName']
        AssistingDoc6FirstName = request.form['AssistingDoc6FirstName']
        AssistingDoc6LastName  = request.form['AssistingDoc6LastName']

        try:
            
            mycursor.execute("SELECT COUNT(ID) FROM Operations")
            myresult1 = mycursor.fetchone()
            OperationID = myresult1[0] + 1

            sql0 = "SELECT ID From Patients WHERE FirstName = %s AND LastName = %s"
            val0 = (PatientFirstName,PatientLastName)
            mycursor.execute(sql0,val0)
            myresult2 = mycursor.fetchone()
            PatientID = myresult2[0]
            

            mainsql = "INSERT INTO Operations (ID , Type , Day , Month , Year , OperationLevel , EstimatedHours , PatientID , LeadingDoctorID, Status ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"
            mainval = (OperationID,OperationType,OperationDay,OperationMonth,OperationYear,OperationLevel,EstimatedHours,PatientID,LeadingDoctorID,"Pending")
            mycursor.execute(mainsql,mainval)
            mydb.commit()

            if ( AssistingDoc1FirstName != "" and AssistingDoc1LastName != "" ):
                sql1 = "SELECT ID From Doctors WHERE FirstName = %s AND LastName = %s"
                val1 = (AssistingDoc1FirstName,AssistingDoc1LastName)
                mycursor.execute(sql1,val1)
                sideresult1 = mycursor.fetchone()
                AssDoc1ID = sideresult1[0]
                sidesql1 = "INSERT INTO AssistingDoctors (OperationID, DoctorID) VALUES ( %s, %s )"
                sideval1 = (OperationID,AssDoc1ID)
                mycursor.execute(sidesql1,sideval1)
                mydb.commit()

            if ( AssistingDoc2FirstName != "" and AssistingDoc2LastName != "" ):
                sql2 = "SELECT ID From Doctors WHERE FirstName = %s AND LastName = %s"
                val2 = (AssistingDoc2FirstName,AssistingDoc2LastName)
                mycursor.execute(sql2,val2)
                sideresult2 = mycursor.fetchone()
                AssDoc2ID = sideresult2[0]
                sidesql2 = "INSERT INTO AssistingDoctors ( OperationID, DoctorID ) VALUES (%s, %s)"
                sideval2 = (OperationID,AssDoc2ID)
                mycursor.execute(sidesql2,sideval2)
                mydb.commit()

            if ( AssistingDoc3FirstName != "" and AssistingDoc3LastName != "" ):
                sql3 = "SELECT ID From Doctors WHERE FirstName = %s AND LastName = %s"
                val3 = (AssistingDoc3FirstName,AssistingDoc3LastName)
                mycursor.execute(sql3,val3)
                sideresult3 = mycursor.fetchone()
                AssDoc3ID = sideresult3[0]
                sidesql3 = "INSERT INTO AssistingDoctors ( OperationID, DoctorID ) VALUES (%s, %s)"
                sideval3 = (OperationID,AssDoc3ID)
                mycursor.execute(sidesql3,sideval3)
                mydb.commit()

            if ( AssistingDoc4FirstName != "" and AssistingDoc4LastName != "" ):
                sql4 = "SELECT ID From Doctors WHERE FirstName = %s AND LastName = %s"
                val4 = (AssistingDoc4FirstName,AssistingDoc4LastName)
                mycursor.execute(sql4,val4)
                sideresult4 = mycursor.fetchone()
                AssDoc4ID = sideresult4[0]
                sidesql4 = "INSERT INTO AssistingDoctors ( OperationID, DoctorID ) VALUES (%s, %s)"
                sideval4 = (OperationID,AssDoc4ID)
                mycursor.execute(sidesql4,sideval4)
                mydb.commit()

            if ( AssistingDoc5FirstName != "" and AssistingDoc5LastName != "" ):
                sql5 = "SELECT ID From Doctors WHERE FirstName = %s AND LastName = %s"
                val5 = (AssistingDoc5FirstName,AssistingDoc5LastName)
                mycursor.execute(sql5,val5)
                sideresult5 = mycursor.fetchone()
                AssDoc5ID = sideresult5[0]
                sidesql5 = "INSERT INTO AssistingDoctors ( OperationID, DoctorID ) VALUES (%s, %s)"
                sideval5 = (OperationID,AssDoc5ID)
                mycursor.execute(sidesql5,sideval5)
                mydb.commit()

            if ( AssistingDoc6FirstName != "" and AssistingDoc6LastName != "" ):
                sql6 = "SELECT ID From Doctors WHERE FirstName = %s AND LastName = %s"
                val6 = (AssistingDoc6FirstName,AssistingDoc6LastName)
                mycursor.execute(sql6,val6)
                sideresult6 = mycursor.fetchone()
                AssDoc6ID = sideresult6[0]
                sidesql6 = "INSERT INTO AssistingDoctors ( OperationID, DoctorID ) VALUES (%s, %s)"
                sideval6 = (OperationID,AssDoc6ID)
                mycursor.execute(sidesql6,sideval6)
                mydb.commit()


            return render_template("ReservationRequestFeedback.html", SuccessMsg1 = "Your Reservation Request has been successfully sent!", SuccessMsg2 = "Your Request is pending approval. Please wait a few hours while the admin reviews your request.", SuccessMsg3 = "Thank you for your patience!")

        except:
            return render_template("ReservationRequestFeedback.html", FailureMsg1 = "Something is wrong with the data you entered!", FailureMsg2 = "Please try again. Thank you.")

    else:
        return render_template("ReservationRequestFormPage.html")

@app.route('/ReservationRequestFeedback')
def ReservationRequestFeedback():
        return render_template("ReservationRequestFeedback.html")

@app.route('/ViewReservationRequests')
def ViewReservationRequests():

    sql1 = "SELECT * FROM Operations WHERE OperationLevel = %s AND Status = %s ORDER BY Year, Month, Day"
    val1 = ("Critical","Pending")
    mycursor.execute(sql1,val1)
    CriticalOps = mycursor.fetchall()

    sql2 = "SELECT * FROM Operations WHERE OperationLevel = %s AND Status = %s ORDER BY Year, Month, Day"
    val2 = ("High","Pending")
    mycursor.execute(sql2,val2)
    HighOps = mycursor.fetchall()

    sql3 = "SELECT * FROM Operations WHERE OperationLevel = %s AND Status = %s ORDER BY Year, Month, Day"
    val3 = ("Medium","Pending")
    mycursor.execute(sql3,val3)
    MediumOps= mycursor.fetchall()

    sql4 = "SELECT * FROM Operations WHERE OperationLevel = %s AND Status = %s ORDER BY Year, Month, Day"
    val4 = ("Low","Pending")
    mycursor.execute(sql4,val4)
    LowOps = mycursor.fetchall()

    return render_template("ViewReservationRequests.html", CriticalOperations = CriticalOps, HighOperations = HighOps, MediumOperations = MediumOps, LowOperations = LowOps )

@app.route('/ViewConfirmationResult', methods=['GET', 'POST'])
def ViewConfirmationResult():
        if request.method == "POST" :

            try:
                #Retrieving ID of Chosen Operation 
                OperationID = request.form['OperationID']

                #Changing its status in Operations table to confirmed
                sql1 = "UPDATE Operations SET Status = %s WHERE ID = %s"
                val1 = ("Confirmed",OperationID)
                mycursor.execute(sql1,val1)
                mydb.commit()

                #Retrieving info of chosen operation
                sql2 = "SELECT * From Operations WHERE ID = %s "
                val2 = (OperationID,)
                mycursor.execute(sql2,val2)
                OperationInfo = mycursor.fetchone()

                OperationDay = int(OperationInfo[2])
                OperationMonth = int(OperationInfo[3])
                OperationYear = int(OperationInfo[4])
                EstimatedHours = int(OperationInfo[6])

                #Retrieving operation room numbers
                mycursor.execute("SELECT RoomNumber FROM OperationRooms")
                ORIDList = mycursor.fetchall()
                NumberofORs = len(ORIDList)

                #Finding a room
                RoomFound = False             
                StartTime = -1
                EndTime = -1
                RoomNumber = -1
                j = 1
                while ( j <= 14 and  RoomFound == False  ):

                    i = 0
                    while ( i < NumberofORs and RoomFound == False ):
                
                        sql = "SELECT StartTime, EstimatedEndTime FROM ConfirmedOperations JOIN Operations ON OperationID = ID WHERE Day = %s AND Month = %s AND Year = %s AND OperationRoomNumber = %s ORDER BY TableInsertionOrder"
                        val = (OperationDay,OperationMonth,OperationYear,ORIDList[i][0])
                        mycursor.execute(sql,val)
                        ListofStartandEndTimesOnThisDayInThisRoom = mycursor.fetchall()
                        NumberofOperationsOnThisDayInThisRoom = len(ListofStartandEndTimesOnThisDayInThisRoom)

                        if ( NumberofOperationsOnThisDayInThisRoom == 0 ):
                            RoomFound = True
                            RoomNumber = ORIDList[i][0]
                            StartTime = 6
                            EndTime = StartTime + EstimatedHours
                        else:
                            EndTimeofLastOperationOnThisDayInThisRoom = ListofStartandEndTimesOnThisDayInThisRoom[NumberofOperationsOnThisDayInThisRoom-1][1]
                            if ( EndTimeofLastOperationOnThisDayInThisRoom < 24 and EndTimeofLastOperationOnThisDayInThisRoom + 1 + EstimatedHours <= 24 ):
                                RoomFound = True
                                RoomNumber = ORIDList[i][0]
                                StartTime = EndTimeofLastOperationOnThisDayInThisRoom + 1
                                EndTime = StartTime + EstimatedHours
                            elif ( EndTimeofLastOperationOnThisDayInThisRoom <= 24 and EndTimeofLastOperationOnThisDayInThisRoom + 1 + EstimatedHours > 24 ):
                                RoomFound = False
                                i += 1
                
                    if ( RoomFound == False ):
                        OperationDay += 1
                        if ( OperationDay >= 31 ):
                            OperationMonth += 1
                            if ( OperationMonth >= 13 ):
                                OperationDay = 1
                                OperationMonth = 1
                                OperationYear += 1
                                if ( OperationYear >= 2031 ):
                                    OperationYear = -1
                        j += 1


                if ( RoomFound == True ):
                    print(OperationDay,'/',OperationMonth,'/',OperationYear)

                    sidesql = "UPDATE Operations SET Day = %s, Month = %s, Year = %s WHERE ID = %s"
                    sideval = (OperationDay, OperationMonth, OperationYear, OperationID)
                    mycursor.execute(sidesql, sideval)
                    mydb.commit()

                    mainsql = "INSERT INTO ConfirmedOperations ( OperationID, StartTime, EstimatedEndTime, OperationRoomNumber ) VALUES (%s, %s, %s, %s)"
                    mainval = (OperationInfo[0], StartTime, EndTime, RoomNumber)
                    mycursor.execute(mainsql, mainval)
                    message =  OperationInfo[0]
                    sync_cal(message,StartTime,EndTime,OperationYear,OperationMonth,OperationDay)
                    mydb.commit()

                return render_template("ViewConfirmationResult.html", OperationInfo = OperationInfo, StartTime = StartTime, EndTime = EndTime, RoomNumber = RoomNumber, success = "succ" )

            except:
                return render_template("ViewConfirmationResult.html", error = "err")

        else: 
            return render_template("ViewConfirmationResult.html")
            
@app.route('/ViewConfirmedOperations')
def ViewConfirmedOperations():
    mycursor.execute("SELECT ID, Type, Day, Month, Year, OperationLevel, StartTime, EstimatedEndTime, OperationRoomNumber, PatientID, LeadingDoctorID, EndingStatus FROM Operations JOIN ConfirmedOperations WHERE ID = OperationID ORDER BY Year, Month, Day, OperationRoomNumber, StartTime")
    ConfirmedOps = mycursor.fetchall()
    return render_template("ViewConfirmedOperations.html", ConfirmedOperations = ConfirmedOps)

@app.route('/PendingRequestedOperations')
def PendingRequestedOperations():
    sql = "SELECT * FROM Operations WHERE Status = %s AND LeadingDoctorID = %s  ORDER BY Year, Month, Day"
    DoctorID = session["DocID"]
    val = ("Pending", DoctorID)
    mycursor.execute(sql,val)
    PendingOps = mycursor.fetchall()
    return render_template("PendingRequestedOperations.html", PendingOperations = PendingOps )

@app.route('/ConfirmedRequestedOperations')
def ConfirmedRequestedOperations():
    sql = "SELECT * FROM Operations JOIN ConfirmedOperations ON ID = OperationID WHERE LeadingDoctorID = %s  ORDER BY Year, Month, Day"
    DoctorID = session["DocID"]
    val = (DoctorID,)
    mycursor.execute(sql,val)
    ConfirmedOps = mycursor.fetchall()
    return render_template("ConfirmedRequestedOperations.html", ConfirmedOperations = ConfirmedOps )

@app.route('/ConfirmedAssistingOperations')
def ConfirmedAssistingOperations():
    sql = "SELECT * FROM Operations JOIN ConfirmedOperations ON ID = ConfirmedOperations.OperationID JOIN AssistingDoctors ON ConfirmedOperations.OperationID = AssistingDoctors.OperationID WHERE DoctorID = %s  ORDER BY Year, Month, Day"
    DoctorID = session["DocID"]
    val = (DoctorID,)
    mycursor.execute(sql,val)
    AssistingOps = mycursor.fetchall()
    return render_template("ConfirmedAssistingOperations.html", AssistingOperations = AssistingOps )

@app.route('/OperationsEndingStatus', methods=['GET', 'POST'])
def OperationsEndingStatus():
    if request.method == "POST" :
        OperationID = request.form['OperationID']
        OperationEndingStatus = request.form['OperationEndingStatus']
        print(OperationID)
        print(OperationEndingStatus)

        try:
            sql = "SELECT * FROM ConfirmedOperations WHERE OperationID = %s"
            val = (OperationID,)
            mycursor.execute(sql,val)
            myresult = mycursor.fetchall()
            if ( len(myresult) == 0 ):
                return render_template("OperationsEndingStatus.html", FailureMsg = "Oops.. You did not enter a valid ID.")

            mainsql = "UPDATE ConfirmedOperations SET EndingStatus = %s WHERE OperationID = %s"
            mainval = (OperationEndingStatus,OperationID)
            mycursor.execute(mainsql,mainval)
            mydb.commit()
            return render_template("OperationsEndingStatus.html", SuccessMsg = "Ending Status Submitted Successfully!")
        except:
            return render_template("OperationsEndingStatus.html", FailureMsg = "Oops.. You did not enter a valid ID.")

    else:
        return render_template("OperationsEndingStatus.html")

@app.route('/ViewYourOperations')
def ViewYourOperations():
    sql = "SELECT Operations.ID, Type, Day, Month, Year, StartTime, EstimatedEndTime, OperationRoomNumber, FirstName, LastName FROM Operations JOIN ConfirmedOperations ON Operations.ID = OperationID JOIN Doctors ON LeadingDoctorID = Doctors.ID WHERE PatientID = %s ORDER BY Year, Month, Day, StartTime"
    PatID = session["PatID"]
    val = (PatID,)
    mycursor.execute(sql,val)
    OpsList = mycursor.fetchall()
    return render_template("ViewYourOperations.html", OperationsList = OpsList)

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
      userID = request.form['userID']
      userpsw = request.form['userpsw']
      mycursor.execute("SELECT * FROM Doctors WHERE ID=%s And PassWord=%s ",
      (userID,userpsw)) 
      myresult = mycursor.fetchall()
      if myresult:   
        session['DocID']=userID
        return redirect(url_for('DocProfile'))
      else:
        error='Incorrect username or password.'

        mycursor.execute("SELECT * FROM Admins WHERE ID=%s And PassWord=%s ",
        (userID,userpsw)) 
        myresult = mycursor.fetchall()
        if myresult:   
          session['admID']=userID
          return redirect(url_for('AdminProfile'))
        else:
          error='Incorrect username or password.'
        
        mycursor.execute("SELECT * FROM Patients WHERE ID=%s And PassWord=%s ",
        (userID,userpsw)) 
        myresult = mycursor.fetchall()
        if myresult:   
          session['PatID']=userID
          return redirect(url_for('PatientProfile'))
        else:
          error='Incorrect username or password.'

        if error:    
          flash(error)
          return render_template('login.html') 
    else:
      return render_template('login.html') 

@app.route('/signup')
def signup():
  return render_template('signup.html') 

@app.route('/Adminsignup', methods=['GET', 'POST'])
def Adminsignup():
  if request.method=="POST":
    admusername=request.form['admusername']
    admID=request.form['admID']
    admpsw= request.form['admpsw']
    admFname=request.form['admFname']
    admLname=request.form['admLname'] 
    admGender=request.form['admGender']
    admNationality=request.form['admnationality']
    admDay=request.form['admDay']
    admMonth=request.form['admMonth']
    admYear=request.form['admYear']
    admemail=request.form['admemail']
    admaddress=request.form['admaddress']
    admMobile=request.form['admMobile']

    error = None
    mycursor.execute('SELECT UserName FROM Admins WHERE ID = %s', (admID,))
    myresult = mycursor.fetchall()
    if "admID" in session:
      return redirect(url_for('AdminProfile'))
    elif not admusername:
      error = 'Username is required.'
    elif not admpsw:
      error = 'Password is required.'
    elif not admemail:
      error = 'Email is required.' 
    elif not admID:
      error = 'ID is required.'
    elif not admFname:
      error='Firstname is required.'
    elif not admLname:
      error='Lastname is required.'
    elif not admGender:
      error='Gender is required.'
    elif not  admNationality:
      error='Nationality is required.'
    elif not admDay:
      error='Day is required.'
    elif not admMonth:
      error='Month is required.'
    elif not admYear:
      error='Year is required.'
    elif not admaddress:
      error='Address is required.'
    elif not admMobile:
      error='admMobile is required.'
    elif myresult :
      error = 'Admin {} is already registered.'.format(admusername)

    if not error :
      mycursor.execute('INSERT INTO Admins (UserName, ID , PassWord,FirstName, LastName,Gender,Nationality ,BDay,BMonth ,BYear, Mobile, Email ,Address) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s)',
      (admusername,admID, admpsw, admFname,admLname,admGender,admNationality,admDay,admMonth,admYear,admMobile,admemail, admaddress ))
      mydb.commit()
      session["admID"]=admID
      x = session["admID"]
      print(x)
      return redirect(url_for('AdminProfile'))
    else:  
      #flash(error)
      return render_template('Adminsignup.html')

  else:
    return render_template('Adminsignup.html')

@app.route('/Docsignup', methods=['GET','POST'])
def Docsignup():
  if request.method=="POST":
    Docusername=request.form['Docusername']
    DocID=request.form['DocID']
    Docpsw= request.form['Docpsw']
    DocFname=request.form['DocFname']
    DocLname=request.form['DocLname'] 
    DocGender=request.form['DocGender']
    DocNationality=request.form['Docnationality']
    DocDay=request.form['DocDay']
    DocMonth=request.form['DocMonth']
    DocYear=request.form['DocYear']
    Docemail=request.form['Docemail']
    Docaddress=request.form['Docaddress']
    DocMobile=request.form['DocMobile']

    error = None
    mycursor.execute('SELECT UserName FROM Doctors WHERE ID = %s', (DocID,))
    myresult = mycursor.fetchall()
    if "DocID" in session:
      return redirect(url_for('DocProfile'))
    elif not Docusername:
      error = 'Username is required.'
    elif not Docpsw:
      error = 'Password is required.'
    elif not Docemail:
      error = 'Email is required.' 
    elif not DocID:
      error = 'ID is required.'
    elif not DocFname:
      error='Firstname is required.'
    elif not DocLname:
      error='Lastname is required.'
    elif not DocGender:
      error='Gender is required.'
    elif not DocNationality:
      error='Nationality is required.'
    elif not DocDay:
      error='Day is required.'
    elif not DocMonth:
      error='Month is required.'
    elif not DocYear:
      error='Year is required.'
    elif not Docaddress:
      error='Address is required.'
    elif not DocMobile:
      error='DocMobile is required.'
    elif myresult :
      error = 'Doctor {} is already registered.'.format(Docusername)

    if not error :
      mycursor.execute('INSERT INTO Doctors (UserName, ID , PassWord,FirstName, LastName,Gender,Nationality ,BDay,BMonth ,BYear, Mobile, Email ,Address) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s)',
      (Docusername,DocID, Docpsw, DocFname,DocLname,DocGender,DocNationality,DocDay,DocMonth,DocYear,DocMobile,Docemail, Docaddress ))
      mydb.commit()
      session["DocID"]=DocID
      x = session["DocID"]
      print(x)
      return redirect(url_for('DocProfile'))
    else:  
      #flash(error)
      return render_template('Docsignup.html')

  else:
    return render_template('Docsignup.html')

@app.route('/Patientsignup', methods=['GET','POST'])
def Patientsignup():
  if request.method=="POST":
    Patusername=request.form['Patusername']
    PatID=request.form['PatID']
    Patpsw= request.form['Patpsw'] 
    PatFname=request.form['PatFname']
    PatLname=request.form['PatLname'] 
    PatGender=request.form['PatGender']
    PatNationality=request.form['Patnationality']
    PatDay=request.form['PatDay']
    PatMonth=request.form['PatMonth']
    PatYear=request.form['PatYear']
    Patemail=request.form['Patemail']
    Pataddress=request.form['Pataddress']
    PatMobile=request.form['PatMobile']
    Weight=request.form['Weight']
    Height=request.form['Height']
    ChronicDiseases=request.form['ChronicDiseases']
    Allergies=request.form['Allergies']
    PreviousOperations=request.form['PreviousOperations']
    error=None
    mycursor.execute('SELECT UserName FROM Patients WHERE ID = %s', (PatID,))
    myresult = mycursor.fetchall()
    if "PatID" in session:
      return redirect(url_for('PatientProfile'))
    elif not Patusername:
      error = 'Username is required.'
    elif not Patpsw:
      error = 'Password is required.'
    elif not Patemail:
      error = 'Email is required.' 
    elif not PatID:
      error = 'ID is required.'
    elif not   Patusername:
      error='Username is required.'
    elif not  PatFname:
      error='Firstname is required.'
    elif not   PatLname:
      error='Lastname is required.'
    elif not  PatGender:
      error='Gender is required.'
    elif not  PatNationality:
      error='Nationality is required.'
    elif not PatDay:
      error='Day is required.'
    elif not PatMonth:
      error='Month is required.'
    elif not PatYear:
      error='Year is required.'
    elif not Pataddress:
      error='Address is required.'
    elif not PatMobile:
      error='PatMobile is required.'
    elif not Weight:
      error='Weight is required.'
    elif not Height:
      error='Height is required.'
    elif not ChronicDiseases:
      error='Chronic Diseases are required.'
    elif not Allergies:
      error='Allergies are required.'
    elif not PreviousOperations:
      error='Previous Operations are required.'
    elif myresult:
      error = 'Patient {} is already registered.'.format(Patusername)
    
    if not error:
      mycursor.execute('INSERT INTO Patients (UserName, ID , PassWord,FirstName, LastName,Gender,Nationality ,BDay,BMonth ,BYear, Mobile, Email ,Address, Weight, Height, ChronicDiseases, Allergies, PreviousOperations) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
      (Patusername,PatID, Patpsw, PatFname,PatLname,PatGender,PatNationality,PatDay,PatMonth,PatYear,PatMobile,Patemail, Pataddress, Weight, Height, ChronicDiseases, Allergies, PreviousOperations))
      mydb.commit()
      session["PatID"]=PatID
      return redirect(url_for('PatientProfile'))
    else:  
      flash(error)
      return render_template('Patientsignup.html')

  else:
    return render_template('Patientsignup.html')

@app.route('/AdminProfile')
def AdminProfile() :
  return render_template('AdminProfile.html')

@app.route('/DocProfile')
def DocProfile() :
  return render_template('DocProfile.html')

@app.route('/PatientProfile')
def PatientProfile() :
  return render_template('PatientProfile.html')

@app.route('/logout')
def logout():
  if 'admID' in session:
    session.pop("admID",None)
  elif 'PatID' in session:
    session.pop("PatID",None)
  elif 'DocID' in session:
    session.pop("DocID",None)  
  return redirect(url_for('HomePage'))

@app.route('/Cancellation', methods=['GET','POST'])
def Cancellation():
  if request.method=="POST":
    Docpsw= request.form['psw']  
    opID=request.form['operationID']
    # session['id'] = opID
    #check if it is in operations table
    mycursor.execute("SELECT * FROM Operations INNER JOIN Doctors ON Operations.LeadingDoctorID=Doctors.ID  WHERE Doctors.PassWord=%s And Operations.ID=%s And Operations.Status !='Cancelled' ",
    (Docpsw,opID)) 
    myresult = mycursor.fetchall()
    if myresult: 
      sql = "UPDATE Operations SET Status = 'Cancelled' WHERE ID= %s"
      opid=(opID,)
      mycursor.execute(sql,opid)
      mydb.commit()
      sql =  "INSERT INTO CancelledOperations ( OperationID,StartTime,EstimatedEndTime,OperationRoomNumber) SELECT  OperationID,StartTime,EstimatedEndTime,OperationRoomNumber \
      From ConfirmedOperations  WHERE  OperationID = %s "
      opid=(opID,)
      mycursor.execute(sql,opid)
      mydb.commit()
      mycursor.execute("DELETE FROM ConfirmedOperations WHERE OperationID=%s",(opID,))
      mydb.commit()
      #Delete from Calendar
      # return to confirmed 
      return render_template('Cancellation.html')
      # , msg="Cancelled successfully")
    else:
      return render_template('Cancellation.html')
      #  error="No Matching Operation")   
  else:
    return render_template('Cancellation.html')

@app.route('/viewcancelled')
def viewcancelled() :
  DocID = session["DocID"]
  mycursor.execute("SELECT * FROM CancelledOperations INNER JOIN Operations ON CancelledOperations.OperationID=Operations.ID \
  INNER JOIN Doctors ON Operations.LeadingDoctorID= Doctors.ID  WHERE Doctors.ID=%s ", (DocID,)) 
  myresult = mycursor.fetchall()
  for x in myresult:
    print(x)
  return render_template("viewcancelled.html",result=myresult) 

@app.route('/docotrsanalysis')
def doctoranalysis():
  # mycursor.execute(" SELECT Type FROM ConfirmedOperations")
  # myresult = mycursor.fetchall()
  # for x in myresult:
  #   print(x)
  sql= " SELECT Doctors.ID, COUNT(*) FROM Doctors INNER JOIN Operations ON Doctors.ID = Operations.LeadingDoctorID INNER JOIN ConfirmedOperations ON Operations.ID=ConfirmedOperations.OperationID WHERE EndingStatus =%s GROUP BY Doctors.ID "
  suc= "Success" 
  val=(suc,)
  mycursor.execute(sql,val)
  myresult = mycursor.fetchall()
  for x in myresult:
    print(x)
  return render_template('doctoranalysis.html',result=myresult)

@app.route('/operationsanalysis')
def operationsanalysis():
  # mycursor.execute(" SELECT Type FROM ConfirmedOperations")
  # myresult = mycursor.fetchall()
  # for x in myresult:
  #   print(x)
  sql= " SELECT Operations.Type, COUNT(*) FROM Operations INNER JOIN ConfirmedOperations ON Operations.ID=ConfirmedOperations.OperationID WHERE EndingStatus =%s GROUP BY Type "
  suc= "Success" 
  val=(suc,)
  mycursor.execute(sql,val)
  myresult = mycursor.fetchall()
  for x in myresult:
    print(x)
  return render_template('operationsanalysis.html',result=myresult)

  #  mycursor.execute("SELECT * FROM Doctors")
  #     row_headers=[x[0] for x in mycursor.description] #this will extract row headers
  #     myresult = mycursor.fetchall()
  #     data={
  #        'message':"data retrieved",
  #        'rec':myresult,
  #        'header':row_headers
  #     }
  #     return render_template('viewdoctor.html',data=data)
@app.route('/AdminUpdate', methods=['GET','POST'])  
def AdminUpdate():
  if request.method=="POST":
    admID=session["admID"]
    admusername=request.form['admusername']
    admpsw= request.form['admpsw']
    admFname=request.form['admFname']
    admLname=request.form['admLname'] 
    admGender=request.form['admGender']
    admNationality=request.form['admnationality']
    admDay=request.form['admDay']
    admMonth=request.form['admMonth']

    admYear=request.form['admYear']

    admemail=request.form['admemail']

    admaddress=request.form['admaddress']

    admMobile=request.form['admMobile']
    # sql= "UPDATE Admins SET UserName=%s , PassWord=%s, FirstName=%s, LastName= %s, Gender=%s, Nationality=%s , Day=%s, Month=%s ,Year =%s, Mobile=%s, Email=%s ,Address= %s  WHERE ID=%s "
    # val=(admusername, admpsw, admFname,admLname,admGender,admNationality,admDay,admMonth,admYear,admMobile,admemail, admaddress, admID )
    # mycursor.execute(sql,val)
    # mydb.commit()
    error=None
    if not admusername:
      error = 'Username is required.'
    elif not admpsw:
      error = 'Password is required.'
    elif not admemail:
      error = 'Email is required.' 
    elif not admID:
      error = 'ID is required.'
    elif not admFname:
      error='Firstname is required.'
    elif not admLname:
      error='Lastname is required.'
    elif not admGender:
      error='Gender is required.'
    elif not admNationality:
      error='Nationality is required.'
    elif not admDay:
      error='Day is required.'
    elif not admMonth:
      error='Month is required.'
    elif not admYear:
      error='Year is required.'
    elif not admaddress:
      error='Address is required.'
    elif not admMobile:
      error='admMobile is required.'
    

    if error:
      return render_template('Admininfo.html',error=error)
    else:

      mycursor.execute("DELETE FROM Admins WHERE ID=%s",(admID,))
      mydb.commit()
      mycursor.execute('INSERT INTO Admins (UserName, ID , PassWord,FirstName, LastName,Gender,Nationality ,BDay,BMonth ,BYear, Mobile, Email ,Address) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s)',
      (admusername,admID, admpsw, admFname,admLname,admGender,admNationality,admDay,admMonth,admYear,admMobile,admemail, admaddress ))
      mydb.commit()
  
      return redirect(url_for('Admininfo'))
  else:
    admID = session["admID"]
    mycursor.execute("SELECT * FROM Admins WHERE Admins.ID=%s ", (admID,)) 
    myresult = mycursor.fetchall()
    return render_template('AdminUpdate.html',result=myresult)

@app.route('/PatientUpdate', methods=['GET','POST'])  
def PatientUpdate():
  if request.method=="POST":
    PatID=session["PatID"]
    Patusername=request.form['Patusername']
    Patpsw= request.form['Patpsw']
    PatFname=request.form['PatFname']
    PatLname=request.form['PatLname'] 
    PatGender=request.form['PatGender']
    PatNationality=request.form['Patnationality']
    PatDay=request.form['PatDay']
    PatMonth=request.form['PatMonth']

    PatYear=request.form['PatYear']

    Patemail=request.form['Patemail']

    Pataddress=request.form['Pataddress']

    PatMobile=request.form['PatMobile']
    Weight=request.form['Weight']
    Height=request.form['Height']
    ChronicDiseases=request.form['ChronicDiseases']
    Allergies=request.form['Allergies']
    PreviousOperations=request.form['PreviousOperations']
    # sql= "UPDATE Patins SET UserName=%s , PassWord=%s, FirstName=%s, LastName= %s, Gender=%s, Nationality=%s , Day=%s, Month=%s ,Year =%s, Mobile=%s, Email=%s ,Address= %s  WHERE ID=%s "
    # val=(Patusername, Patpsw, PatFname,PatLname,PatGender,PatNationality,PatDay,PatMonth,PatYear,PatMobile,Patemail, Pataddress, PatID )
    # mycursor.execute(sql,val)
    # mydb.commit()
    error=None
    if not Patusername:
      error = 'Username is required.'
    elif not Patpsw:
      error = 'Password is required.'
    elif not Patemail:
      error = 'Email is required.' 
    elif not PatID:
      error = 'ID is required.'
    elif not PatFname:
      error='Firstname is required.'
    elif not PatLname:
      error='Lastname is required.'
    elif not PatGender:
      error='Gender is required.'
    elif not PatNationality:
      error='Nationality is required.'
    elif not PatDay:
      error='Day is required.'
    elif not PatMonth:
      error='Month is required.'
    elif not PatYear:
      error='Year is required.'
    elif not Pataddress:
      error='Address is required.'
    elif not PatMobile:
      error='PatMobile is required.'
    elif not Weight:
      error='Weight is required.'
    elif not Height:
      error='Height is required.'
    elif not ChronicDiseases:
      error='Chronic Diseases are required.'
    elif not Allergies:
      error='Allergies are required.'
    elif not PreviousOperations:
      error='Previous Operations are required.'

    if error:
      return render_template('Patinfo.html',error=error)
    else:

      mycursor.execute("DELETE FROM Patients WHERE ID=%s",(PatID,))
      mydb.commit()
      mycursor.execute('INSERT INTO Patients (UserName, ID , PassWord,FirstName, LastName,Gender,Nationality ,BDay,BMonth ,BYear, Mobile, Email ,Address) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s)',
      (Patusername,PatID, Patpsw, PatFname,PatLname,PatGender,PatNationality,PatDay,PatMonth,PatYear,PatMobile,Patemail, Pataddress ))
      mydb.commit()
  
      return redirect(url_for('Patinfo'))
  else:
    PatID = session["PatID"]
    mycursor.execute("SELECT * FROM Patins WHERE Patients.ID=%s ", (PatID,)) 
    myresult = mycursor.fetchall()
    return render_template('PatientUpdate.html',result=myresult)
@app.route('/DocUpdate', methods=['GET','POST'])  
def DocUpdate():
  if request.method=="POST":
    DocID=session["DocID"]
    Docusername=request.form['Docusername']
    Docpsw= request.form['Docpsw']
    DocFname=request.form['DocFname']
    DocLname=request.form['DocLname'] 
    DocGender=request.form['DocGender']
    DocNationality=request.form['Docnationality']
    DocDay=request.form['DocDay']
    DocMonth=request.form['DocMonth']

    DocYear=request.form['DocYear']

    Docemail=request.form['Docemail']

    Docaddress=request.form['Docaddress']

    DocMobile=request.form['DocMobile']
    # sql= "UPDATE Docotrs SET UserName=%s , PassWord=%s, FirstName=%s, LastName= %s, Gender=%s, Nationality=%s , Day=%s, Month=%s ,Year =%s, Mobile=%s, Email=%s ,Address= %s  WHERE ID=%s "
    # val=(Docusername, Docpsw, DocFname,DocLname,DocGender,DocNationality,DocDay,DocMonth,DocYear,DocMobile,Docemail, Docaddress, DocID )
    # mycursor.execute(sql,val)
    # mydb.commit()
    error=None
    if not Docusername:
      error = 'Username is required.'
    elif not Docpsw:
      error = 'Password is required.'
    elif not Docemail:
      error = 'Email is required.' 
    elif not DocID:
      error = 'ID is required.'
    elif not DocFname:
      error='Firstname is required.'
    elif not DocLname:
      error='Lastname is required.'
    elif not DocGender:
      error='Gender is required.'
    elif not DocNationality:
      error='Nationality is required.'
    elif not DocDay:
      error='Day is required.'
    elif not DocMonth:
      error='Month is required.'
    elif not DocYear:
      error='Year is required.'
    elif not Docaddress:
      error='Address is required.'
    elif not DocMobile:
      error='DocMobile is required.'
    

    if error:
      return render_template('Docinfo.html',error=error)
    else:

      mycursor.execute("DELETE FROM Doctors WHERE ID=%s",(DocID,))
      mydb.commit()
      mycursor.execute('INSERT INTO Doctors (UserName, ID , PassWord,FirstName, LastName,Gender,Nationality ,Day,Month ,Year, Mobile, Email ,Address) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s)',
      (Docusername,DocID, Docpsw, DocFname,DocLname,DocGender,DocNationality,DocDay,DocMonth,DocYear,DocMobile,Docemail, Docaddress ))
      mydb.commit()
  
      return redirect(url_for('Docinfo'))
  else:
    DocID = session["DocID"]
    mycursor.execute("SELECT * FROM Doctors WHERE Doctors.ID=%s ", (DocID,)) 
    myresult = mycursor.fetchall()
    return render_template('DocUpdate.html',result=myresult)

@app.route('/Admininfo')
def Admininfo() :
  if"admID" in session:
    admID = session["admID"]
    mycursor.execute("SELECT * FROM Admins WHERE ID=%s ", (admID,)) 
    myresult = mycursor.fetchall()
    return render_template('Admininfo.html',result=myresult)
  else:  
    return render_template('login.html')
    

@app.route('/Docinfo')
def Docinfo() :
  if"DocID" in session:
    DocID = session["DocID"]
    mycursor.execute("SELECT * FROM Doctors WHERE Doctors.ID=%s ", (DocID,)) 
    myresult = mycursor.fetchall()
    return render_template("Docinfo.html",result=myresult)
  else:
    return render_template('login.html') 

@app.route('/Patinfo')
def Patinfo() :
  if"PatID" in session:
    PatID = session["PatID"]
    mycursor.execute("SELECT * FROM Patients WHERE ID=%s ", (PatID,)) 
    myresult = mycursor.fetchall()
    return render_template("Patinfo.html",result=myresult)
  else:
    return render_template('login.html')

@app.route('/DeleteDoctororPatient')
def DeleteDoctororPatient() :
  mycursor.execute("SELECT ID, FirstName, LastName, Mobile, Email FROM Doctors")
  Docs = mycursor.fetchall()
  mycursor.execute("SELECT ID, FirstName, LastName, Mobile, Email FROM Patients")
  Pats = mycursor.fetchall()
  return render_template('DeleteDoctororPatient.html', Doctors = Docs, Patients = Pats )

@app.route('/ViewDeleteDoctorResult', methods=['GET', 'POST'])
def ViewDeleteDoctorResult() :
  if request.method == "POST" :
     DoctorID = request.form['DoctorID']
     sql1 = "SELECT * FROM Doctors WHERE ID = %s"
     val1 = (DoctorID,)
     mycursor.execute(sql1,val1)
     Doctor = mycursor.fetchall()
     if ( len(Doctor) == 0 ):
      return render_template('ViewDeleteDoctorResult.html', error = "Doctor Not Deleted!" )
     else:
      sql2 = "DELETE FROM Doctors WHERE ID = %s"
      val2 = (DoctorID,)
      mycursor.execute(sql2,val2)
      mydb.commit()
      return render_template('ViewDeleteDoctorResult.html', success = "Doctor Deleted!" )
  else:
    return render_template('ViewDeleteDoctorResult.html')

@app.route('/ViewDeletePatientResult', methods=['GET', 'POST'])
def ViewDeletePatientResult() :
  if request.method == "POST" :
     PatientID = request.form['PatientID']
     sql1 = "SELECT * FROM Patients WHERE ID = %s"
     val1 = (PatientID,)
     mycursor.execute(sql1,val1)
     Patient= mycursor.fetchall()
     if ( len(Patient) == 0 ):
       return render_template('ViewDeletePatientResult.html', error = "Patient Not Deleted!" )
     else:
      sql2 = "DELETE FROM Patients WHERE ID = %s"
      val2 = (PatientID,)
      mycursor.execute(sql2,val2)
      mydb.commit()
      return render_template('ViewDeletePatientResult.html', success = "Patient Deleted!" )
  else:
    return render_template('ViewDeletePatientResult.html')

if __name__ == '__main__':
   app.run()
