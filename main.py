import uuid
import sqlite3
import requests
import json
import datetime
import build
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

now = datetime.datetime.now()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
    mem_conn = sqlite3.connect(':memory:')

    mem_conn.execute('''

    create table OrganizationalUnits (
    	OrgUnitIdentifier int
    	,Name TEXT
    	,Acronym  TEXT
    	,ParentIdentifier  int
    	,Type  TEXT
    );
    ''')
    mem_conn.execute('''

    create table AcademicTerm (
    	TermIdentifier int
    	,Name TEXT
    	,BeginDate  datetime
    	,EndDate datetime
    	,ParentIdentifier int
    	,Type TEXT
    );
    ''')
    mem_conn.execute('''

    create table Course (
    	CourseIdentifier  int
    	,Subject TEXT
    	,CourseNumber TEXT
    	,Title TEXT
    	,Credits float
    	,OrgUnitIdentifier int
    	,CourseType TEXT
    	,Description TEXT
    	,CIPCode TEXT
    );
    ''')
    mem_conn.execute('''

    create table Sections (
    	SectionIdentifier int
    	,TermIdentifier int
    	,CourseIdentifier int
    	,Subject TEXT
    	,CourseNumber TEXT
    	,SectionNumber TEXT
    	,BeginDate datetime
    	,EndDate datetime
    	,OrgUnitIdentifier int
    	,Title TEXT
    	,Credits float
    	,DeliveryMode TEXT
    	,Location TEXT
    	,Description TEXT
    	,CrossListingIdentifier int
    );
    ''')
    mem_conn.execute('''

    create table Attribute (
    	Identifier int
    	,Key TEXT
    	,Value TEXT
    );
    ''')
    mem_conn.execute('''

    create table Instructors (
    	PersonIdentifier int
    	,SectionIdentifier int
    	,FirstName TEXT
    	,LastName TEXT
    	,Email TEXT
    	,Role TEXT
    );
    ''')
    mem_conn.execute('''

    create table Enrollments (
    	PersonIdentifier int
    	,SectionIdentifier int
    	,Status  TEXT
    	,FirstName TEXT
    	,LastName TEXT
    	,Email TEXT
    	,Credits float
    	,GradeOption TEXT
    	,RegisteredDate datetime
    	,BeginDate datetime
    	,EndDate datetime
    	,InitialCourseGrade  TEXT
    	,StatusChangeDate datetime
    	,FinalCourseGrade TEXT
    );
    ''')
    mem_conn.execute('''

    create table RemoveInstructor (
    	PersonIdentifier int
    	,SectionIdentifier int
    );
    ''')
    mem_conn.execute('''

    create table AcademicPrograms (
    	ProgramIdentifier int
    	,OrgUnitIdentifier int
    	,Name TEXT
    	,ProgramType TEXT
    	,Description TEXT
    	,CourseIdentifiers int
    );

    ''')

    root_uri = "https://sisclientweb-100542.campusnexus.cloud/"

    with requests.Session() as s:
        # set authentication header
        s.auth = (build.odata_username, build.odata_password)

        programs_uri = "{0}ds/campusnexus/StudentCourseStudentEnrollmentPeriods?$expand=" \
                            "StudentCourse($select=CourseId), StudentEnrollmentPeriod($select=Id)," \
                            "StudentEnrollmentPeriod($expand=" \
                                "ProgramVersion($select=Code,Name),Program($select=Id,Code,Name)," \
                                "ProgramVersion($expand=Degree($select=Id,GraduateLevel,Name)))&$select=Id" \
                        "&$filter=StudentCourse/Term/EndDate gt {1} and StudentCourse/Term/StartDate le {2} " \
                        "".format(root_uri, now.strftime("%Y-%m-%d"),
                                  (now + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))

        print(programs_uri)
        r = s.get(programs_uri)
        r.raise_for_status()

        # result = r.json()
        result = json.loads(r.text)
        for child in result.get("value"):
            print(child)
            level = child["StudentEnrollmentPeriod"]["ProgramVersion"]["Degree"]["GraduateLevel"],
            mem_conn.execute("insert into AcademicPrograms(ProgramIdentifier ,OrgUnitIdentifier ,Name ,ProgramType "
            ",Description ,CourseIdentifiers) values (?,?,?,?,?,?)", (
                             child["StudentEnrollmentPeriod"]["Program"]["Id"],
                             child["StudentEnrollmentPeriod"]["ProgramVersion"]["Degree"]["Id"],
                             child["StudentEnrollmentPeriod"]["ProgramVersion"]["Code"],
                             "Undergraduate" if level == 0 else "Graduate",
                             child["StudentEnrollmentPeriod"]["ProgramVersion"]["Name"],
                             child["StudentCourse"]["CourseId"]
            )
            )

        cur = mem_conn.cursor()
        cur.execute(
            "select ProgramIdentifier, OrgUnitIdentifier, Name, ProgramType,Description, group_concat(CourseIdentifiers) "
            "from AcademicPrograms "
            "group by ProgramIdentifier, OrgUnitIdentifier, Name, ProgramType, Description "
            "")
        rows = cur.fetchall()
        with open('AcademicPrograms.csv', 'w') as f:
            for row in rows:
                program_Identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "Program/" + str(row[0])))
                OrgUnitIdentifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "Org/" + str(row[1])))
                Name = row[2]
                Type = row[3]
                Description = row[4]
                CourseIdentifiers = list(map(lambda param_x:str(uuid.uuid3(uuid.NAMESPACE_URL, "Course/" + str(param_x))),  row[5].split(",")))
                print(",".join((program_Identifier, OrgUnitIdentifier, Name, Type, Description, ",".join(CourseIdentifiers))), file=f)



        enrollments_uri = "{0}ds/campusnexus/StudentCourses?$expand=Student($select=FirstName,LastName,EmailAddress)" \
                          "&$filter=EndDate gt {1} and StartDate le {2}" \
                          "&$select=StudentId,ClassSectionId,Status" \
                       "".format(root_uri, now.strftime("%Y-%m-%d"),
                                 (now + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))

        print(enrollments_uri)
        r = s.get(enrollments_uri)
        r.raise_for_status()

        # result = r.json()
        result = json.loads(r.text)
        for child in result.get("value"):
            print(child)
            mem_conn.execute("insert into Enrollments(PersonIdentifier, SectionIdentifier, Status, FirstName"
                             ", LastName, Email) values (?,?,?,?,?,?)", (
                                 child["StudentId"],
                                 child["ClassSectionId"],
                                 child["Status"],
                                 child["Student"]["FirstName"],
                                 child["Student"]["LastName"],
                                 child["Student"]["EmailAddress"],
            )
                             )

        cur = mem_conn.cursor()
        cur.execute(
            "select PersonIdentifier, SectionIdentifier, Status, FirstName, LastName, Email "
            "from Enrollments "
            "")
        rows = cur.fetchall()
        with open('Enrollments.csv', 'w') as f:
            for row in rows:
                person_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "Student/" + str(row[0])))
                section_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "Section/" + str(row[1])))
                status = row[2]
                first_name = row[3]
                last_name = row[4]
                email = row[5]
                print(",".join((person_identifier, section_identifier, status, first_name, last_name, email)), file=f)
