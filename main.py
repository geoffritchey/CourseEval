import re
import uuid
import sqlite3
import requests
import json
import datetime
import build

now = datetime.datetime.now()
course_name = re.compile(r'(\D+)(\d+)')

if __name__ == '__main__':
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

    '''
            Academic Programs
    '''
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
            # print(child)
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

        '''
                Enrollments
        '''
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
            # print(child)
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

            '''
                    Instructors
            '''
            instructor_uri = "{0}ds/campusnexus/StudentCourses?$expand=ClassSection($select=Id)," \
                          "ClassSection($expand=Instructor($select=StaffId)," \
                          "Instructor($expand=Staff($select=FirstName,LastName,EmailAddress)))" \
                          "&$filter=EndDate gt {1} and StartDate le {2}" \
                              "&$select=StudentId&$apply=groupby((ClassSection/Instructor/StaffId))" \
                              "".format(root_uri, now.strftime("%Y-%m-%d"),
                                        (now + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))

            print(instructor_uri)
            r = s.get(instructor_uri)
            r.raise_for_status()

            # result = r.json()
            result = json.loads(r.text)
            for child in result.get("value"):
                # print(child)
                mem_conn.execute("insert into Instructors(PersonIdentifier, SectionIdentifier, FirstName, LastName, Email, Role) values (?,?,?,?,?,?)", (
                                     child["ClassSection"]["Instructor"]["StaffId"],
                                     child["ClassSection"]["Id"],
                                     child["ClassSection"]["Instructor"]["Staff"]["FirstName"],
                                     child["ClassSection"]["Instructor"]["Staff"]["LastName"],
                                     child["ClassSection"]["Instructor"]["Staff"]["EmailAddress"],
                                    "Primary")
                                 )

            cur = mem_conn.cursor()
            cur.execute(
                "select distinct PersonIdentifier, SectionIdentifier, FirstName, LastName, Email, Role "
                "from Instructors "
                "")
            rows = cur.fetchall()
            with open('Instructors.csv', 'w') as f:
                for row in rows:
                    person_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "Staff/" + str(row[0])))
                    section_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "Section/" + str(row[1])))
                    first_name = row[2]
                    last_name = row[3]
                    email = row[4]
                    print(",".join((person_identifier, section_identifier, first_name, last_name, email)), file=f)

            '''
                    Sections
            '''
            sections_uri = "{0}ds/campusnexus/StudentCourses?$expand=ClassSection($select=SectionCode)," \
                             "ClassSection($expand=DeliveryMethod($select=Code)),Term($select=StartDate,EndDate)" \
                             "&$select=Id, StudentId, TermId, CourseId" \
                             "&$filter=EndDate gt {1} and StartDate le {2}"\
                             "".format(root_uri, now.strftime("%Y-%m-%d"),
                                       (now + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))

            print(sections_uri)
            r = s.get(sections_uri)
            r.raise_for_status()

            # result = r.json()
            result = json.loads(r.text)
            for child in result.get("value"):
                # print(child)
                mem_conn.execute("insert into Sections(SectionIdentifier, TermIdentifier, CourseIdentifier"
                                 ", SectionNumber, BeginDate, EndDate, DeliveryMode) values (?,?,?,?,?,?,?)", (
                    child["Id"],
                    child["TermId"],
                    child["CourseId"],
                    child["ClassSection"]["SectionCode"],
                    child["Term"]["StartDate"],
                    child["Term"]["EndDate"],
                    "Online" if child["ClassSection"]["DeliveryMethod"]["Code"] == "ONLINE"
                    else "Face2Face" if child["ClassSection"]["DeliveryMethod"]["Code"] == "ONGOUND" else "Hybrid",
                )
                                 )

            cur = mem_conn.cursor()
            cur.execute(
                "select SectionIdentifier, TermIdentifier, CourseIdentifier, SectionNumber, BeginDate, EndDate, DeliveryMode "
                "from Sections "
                "")
            rows = cur.fetchall()
            with open('Sections.csv', 'w') as f:
                for row in rows:
                    section_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "Section/" + str(row[0])))
                    term_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "Term/" + str(row[1])))
                    course_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "Course/" + str(row[2])))
                    number = row[3]
                    begin_date = row[4]
                    end_date = row[5]
                    delivery_mode = row[6]
                    print(",".join((section_identifier, term_identifier, course_identifier, number, begin_date, end_date, delivery_mode)), file=f)


            '''
                    Course
            '''
            course_uri = "{0}ds/campusnexus/StudentCourseStudentEnrollmentPeriods?$expand=StudentCourse($select=Course),StudentCourse($expand=Course($expand=CourseLevel($select=Name)),Course($select=Id,Code,Name)),StudentEnrollmentPeriod($select=ProgramVersion),StudentEnrollmentPeriod($expand=Program($select=Code,Name)),StudentEnrollmentPeriod($expand=ProgramVersion($select=Degree),ProgramVersion($expand=Degree($select=Id)))" \
                         "&$filter=StudentCourse/Term/EndDate gt {1} and StudentCourse/Term/StartDate le {2}" \
                         "&$select=StudentCourse" \
                           "".format(root_uri, now.strftime("%Y-%m-%d"),
                                     (now + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))



            print(course_uri)
            r = s.get(course_uri)
            r.raise_for_status()

            undergrad = set(['Freshman', 'Junior', 'Senior', 'Sophomore'])
            # result = r.json()
            result = json.loads(r.text)
            for child in result.get("value"):
                # print(child)

                m = course_name.match(child["StudentCourse"]["Course"]["Code"])
                mem_conn.execute("insert into Course(CourseIdentifier, Subject, CourseNumber, Title,  OrgUnitIdentifier, CourseType) values (?,?,?,?,?,?)", (
                                     child["StudentCourse"]["Course"]["Id"],
                                     m.group(1),
                                     m.group(2),
                                     child["StudentCourse"]["Course"]["Name"],
                                     child["StudentEnrollmentPeriod"]["Program"]["Code"],
                                     'Undergraduate' if child["StudentCourse"]["Course"]["CourseLevel"]["Name"] in undergrad else 'Graduate',
                )
                                 )

            cur = mem_conn.cursor()
            cur.execute(
                "select CourseIdentifier, Subject, CourseNumber, Title,  OrgUnitIdentifier, CourseType "
                "from Course "
                "")
            rows = cur.fetchall()
            with open('Course.csv', 'w') as f:
                for row in rows:
                    course_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "Course/" + str(row[0])))
                    subject = row[1]
                    number = row[2]
                    title = row[3]
                    org_unit_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "Org/" + str(row[4])))
                    course_type = row[5]
                    print(",".join((course_identifier, subject, number, title, org_unit_identifier, course_type)), file=f)

            '''
                    Terms
            '''
            terms_uri = "{0}ds/campusnexus/Terms?$select=Id,Name,StartDate,EndDate" \
                         "&$filter=EndDate gt {1} and StartDate le {2}" \
                         "".format(root_uri, now.strftime("%Y-%m-%d"),
                                   (now + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))



            print(terms_uri)
            r = s.get(terms_uri)
            r.raise_for_status()

            # result = r.json()
            result = json.loads(r.text)
            for child in result.get("value"):
                # print(child)

                mem_conn.execute("insert into AcademicTerm(TermIdentifier, Name, BeginDate, EndDate, Type) values (?,?,?,?,?)", (
                    child["Id"],
                    child["Name"],
                    child["StartDate"],
                    child["EndDate"],
                    "Semester",
                )
                                 )

            cur = mem_conn.cursor()
            cur.execute(
                "select TermIdentifier, Name, BeginDate, EndDate, Type "
                "from AcademicTerm "
                "")
            rows = cur.fetchall()
            with open('AcademicTerm.csv', 'w') as f:
                for row in rows:
                    term_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "Term/" + str(row[0])))
                    name = row[1]
                    begin_date = row[2]
                    end_date = row[3]
                    type = row[4]
                    print(",".join((term_identifier, name, begin_date, end_date, type)), file=f)

            '''
                    Organizational Units
            '''
            org_unit_uri = "{0}ds/campusnexus/StudentCourseStudentEnrollmentPeriods?$expand=StudentEnrollmentPeriod,StudentEnrollmentPeriod($expand=Program($select=Code,Name)),StudentEnrollmentPeriod($select=Program)&$select=StudentEnrollmentPeriod,StudentCourse" \
                        "&$filter=StudentCourse/Term/EndDate gt {1} and StudentCourse/Term/StartDate le {2}" \
                        "".format(root_uri, now.strftime("%Y-%m-%d"),
                                  (now + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))



            print(org_unit_uri)
            r = s.get(org_unit_uri)
            r.raise_for_status()

            # result = r.json()
            result = json.loads(r.text)
            for child in result.get("value"):
                print(child)

                mem_conn.execute("insert into OrganizationalUnits(OrgUnitIdentifier, Name, Acronym, Type) values (?,?,?,?)", (
                    child["StudentEnrollmentPeriod"]["Program"]["Code"],
                    child["StudentEnrollmentPeriod"]["Program"]["Name"],
                    child["StudentEnrollmentPeriod"]["Program"]["Code"],
                    "Department",
                )
                                 )

            cur = mem_conn.cursor()
            cur.execute(
                "select distinct OrgUnitIdentifier, Name, Acronym, Type "
                "from OrganizationalUnits "
                "")
            rows = cur.fetchall()
            with open('OrganizationalUnits.csv', 'w') as f:
                for row in rows:
                    org_unit_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "Org/" + str(row[0])))
                    name = row[1]
                    acronym = row[2]
                    type = row[3]
                    print(",".join((org_unit_identifier, name, acronym, type)), file=f)
