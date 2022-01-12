import re
import uuid
import sqlite3
import requests
import json
import datetime
import build

now = datetime.datetime.now()
course_name = re.compile(r'(\D+)(\d+)')
top="&$top=10&$count=true"

if __name__ == '__main__':
    mem_conn = sqlite3.connect(':memory:')

    mem_conn.execute('''

    create table AccountData (
    	PersonIdentifier int
    	,FirstName TEXT
    	,LastName  TEXT
    	,Email  TEXT
    );
    ''')

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
    mem_conn.execute('''
    
create table FacultyDemographics (
    ExternalId int
    ,PersonIdentifier int
    ,EffectiveOn datetime
    ,FirstName TEXT
    ,LastName TEXT
    ,EmailAddress1 TEXT
    ,EmailAddress1IsPreferred boolean
    ,EmailAddress2 TEXT
    ,EmailAddress2IsPreferred boolean
    ,EmailAddress3 TEXT
    ,EmailAddress3IsPreferred boolean
    ,PreferredFirstName TEXT
    ,MiddleName TEXT
    ,Suffix TEXT
    ,DateOfBirth datetime
    ,Gender TEXT
    ,Sex TEXT
    ,Race1 TEXT
    ,Race2 TEXT
    ,Race3 TEXT
    ,Ethnicity1 TEXT
    ,Ethnicity2 TEXT
    ,Ethnicity3 TEXT
    ,PrivacyElected boolean
    ,PrimaryDepartment TEXT
    ,Qualifications TEXT
    ,RetiredOn date
    ,TeachingStatus TEXT
    ,Title TEXT
    ,Address1AddressType TEXT
    ,Address1Line1 TEXT
    ,Address1Line2 TEXT
    ,Address1Line3 TEXT
    ,Address1City TEXT
    ,Address1State TEXT
    ,Address1County TEXT
    ,Address1Country TEXT
    ,Address1PostalCode TEXT
    ,Address2AddressType TEXT
    ,Address2Line1 TEXT
    ,Address2Line2 TEXT
    ,Address2Line3 TEXT
    ,Address2City TEXT
    ,Address2State TEXT
    ,Address2County TEXT
    ,Address2Country TEXT
    ,Address2PostalCode TEXT
    ,Address3AddressType TEXT
    ,Address3Line1 TEXT
    ,Address3Line2 TEXT
    ,Address3Line3 TEXT
    ,Address3City TEXT
    ,Address3State TEXT
    ,Address3County TEXT
    ,Address3Country TEXT
    ,Address3PostalCode TEXT
    ,Campus1 TEXT
    ,Campus2 TEXT
    ,Campus3 TEXT
    ,Telephone1CountryCode int
    ,Telephone1AreaCode int
    ,Telephone1Number int
    ,Telephone1Extension int
    ,Telephone1TelephoneType TEXT
    ,Telephone1MobileCarrier TEXT
    ,Telephone2CountryCode int
    ,Telephone2AreaCode int
    ,Telephone2Number int
    ,Telephone2Extension int
    ,Telephone2TelephoneType TEXT
    ,Telephone2MobileCarrier TEXT
    ,Telephone3CountryCode int
    ,Telephone3AreaCode int
    ,Telephone3Number int
    ,Telephone3Extension int
    ,Telephone3TelephoneType TEXT
    ,Telephone3MobileCarrier TEXT
    ,Username1 TEXT
    ,Username2 TEXT
    ,Username3 TEXT
    ,Certification1 TEXT
    ,Certification2 TEXT
    ,Certification3 TEXT
    ,Discipline1 TEXT
    ,Discipline2 TEXT
    ,Discipline3 TEXT
    ,Department1 TEXT
    ,Department2 TEXT
    ,Department3 TEXT
    ,Position1 TEXT
    ,Position2 TEXT
    ,Position3 TEXT
    ,ManagingDepartment1 TEXT
    ,ManagingDepartment2 TEXT
    ,ManagingDepartment3 TEXT
    ,School1 TEXT
    ,School2 TEXT
    ,School3 TEXT
);

    ''')
    mem_conn.execute('''
    
create table StudentDemographics (
    ExternalId int
    ,PersonIdentifier int
    ,EffectiveOn datetime
    ,FirstName TEXT
    ,LastName TEXT
    ,EmailAddress1 TEXT
    ,EmailAddress1IsPreferred boolean
    ,EmailAddress2 TEXT
    ,EmailAddress2IsPreferred boolean
    ,EmailAddress3 TEXT
    ,EmailAddress3IsPreferred boolean
    ,PreferredFirstName TEXT
    ,MiddleName TEXT
    ,Suffix TEXT
    ,DateOfBirth datetime
    ,Gender TEXT
    ,Sex TEXT
    ,Race1 TEXT
    ,Race2 TEXT
    ,Race3 TEXT
    ,Ethnicity1 TEXT
    ,Ethnicity2 TEXT
    ,Ethnicity3 TEXT
    ,CardId int
    ,SisId int
    ,StudentId int
    ,HousingFacility TEXT
    ,PrivacyElected boolean
    ,ActCompositeScore int
    ,ActEnglishScore int
    ,ActMathScore int
    ,ActReadingScore int
    ,ActScienceScore int
    ,ActWritingScore int
    ,SatScore int
    ,SatMathScore int
    ,SatVerbalScore int
    ,SatWritingScore int
    ,GreScore int
    ,GmatScore int
    ,LsatScore int
    ,McatScore int
    ,IncomingGpa numeric
    ,CumulativeGpa numeric
    ,IsMatriculating boolean
    ,Certificate1 TEXT
    ,Certificate2 TEXT
    ,Certificate3 TEXT
    ,Major1 TEXT
    ,Major2 TEXT
    ,Major3 TEXT
    ,Minor1 TEXT
    ,Minor2 TEXT
    ,Minor3 TEXT
    ,Concentration1 TEXT
    ,Concentration2 TEXT
    ,Concentration3 TEXT
    ,DegreeProgram1 TEXT
    ,DegreeProgram2 TEXT
    ,DegreeProgram3 TEXT
    ,SchoolOfEnrollment1 TEXT
    ,SchoolOfEnrollment2 TEXT
    ,SchoolOfEnrollment3 TEXT
    ,DegreeType1 TEXT
    ,DegreeType2 TEXT
    ,DegreeType3 TEXT
    ,AcademicStanding TEXT
    ,AnticipatedGraduationDate date
    ,CareerLevel TEXT
    ,ClassStanding TEXT
    ,CumulativeCreditHoursAttempted int
    ,CumulativeCreditHoursCompleted int
    ,CumulativeCreditsEarned int
    ,CurrentCreditLoad int
    ,EnrollmentStatus TEXT
    ,InstitutionEntryTerm TEXT
    ,PreviousInstitution1Name TEXT
    ,PreviousInstitution1StartDate date
    ,PreviousInstitution1EndDate date
    ,PreviousInstitution2Name TEXT
    ,PreviousInstitution2StartDate date
    ,PreviousInstitution2EndDate date
    ,PreviousInstitution3Name TEXT
    ,PreviousInstitution3StartDate date
    ,PreviousInstitution3EndDate date
    ,AthleticProgram1 TEXT
    ,AthleticProgram2 TEXT
    ,AthleticProgram3 TEXT
    ,HonorsProgram1 TEXT
    ,HonorsProgram2 TEXT
    ,HonorsProgram3 TEXT
    ,FamilyMember1EducationLevel TEXT
    ,FamilyMember1Relationship TEXT
    ,FamilyMember2EducationLevel TEXT
    ,FamilyMember2Relationship TEXT
    ,FamilyMember3EducationLevel TEXT
    ,FamilyMember3Relationship TEXT
    ,PreEntryProgram1 TEXT
    ,PreEntryProgram2 TEXT
    ,PreEntryProgram3 TEXT
    ,LocalResidenceLocation1 TEXT
    ,LocalResidenceLocation2 TEXT
    ,LocalResidenceLocation3 TEXT
    ,AspiredEducationLevel TEXT
    ,ForeignNationalStatus TEXT
    ,HighSchool TEXT
    ,HomeResidenceLocation TEXT
    ,Hometown TEXT
    ,ImmigrationStatus TEXT
    ,IsCommuter boolean
    ,IsFirstGeneration boolean
    ,IsPellGrantEligible boolean
    ,MilitaryStatus TEXT
    ,Address1AddressType TEXT
    ,Address1Line1 TEXT
    ,Address1Line2 TEXT
    ,Address1Line3 TEXT
    ,Address1City TEXT
    ,Address1State TEXT
    ,Address1County TEXT
    ,Address1Country TEXT
    ,Address1PostalCode TEXT
    ,Address2AddressType TEXT
    ,Address2Line1 TEXT
    ,Address2Line2 TEXT
    ,Address2Line3 TEXT
    ,Address2City TEXT
    ,Address2State TEXT
    ,Address2County TEXT
    ,Address2Country TEXT
    ,Address2PostalCode TEXT
    ,Address3AddressType TEXT
    ,Address3Line1 TEXT
    ,Address3Line2 TEXT
    ,Address3Line3 TEXT
    ,Address3City TEXT
    ,Address3State TEXT
    ,Address3County TEXT
    ,Address3Country TEXT
    ,Address3PostalCode TEXT
    ,Campus1 TEXT
    ,Campus2 TEXT
    ,Campus3 TEXT
    ,Telephone1CountryCode int
    ,Telephone1AreaCode int
    ,Telephone1Number int
    ,Telephone1Extension int
    ,Telephone1TelephoneType TEXT
    ,Telephone1MobileCarrier TEXT
    ,Telephone2CountryCode int
    ,Telephone2AreaCode int
    ,Telephone2Number int
    ,Telephone2Extension int
    ,Telephone2TelephoneType TEXT
    ,Telephone2MobileCarrier TEXT
    ,Telephone3CountryCode int
    ,Telephone3AreaCode int
    ,Telephone3Number int
    ,Telephone3Extension int
    ,Telephone3TelephoneType TEXT
    ,Telephone3MobileCarrier TEXT
    ,Username1 TEXT
    ,Username2 TEXT
    ,Username3 TEXT
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
            print(",".join(("ProgramIdentifier", "OrgUnitIdentifier", "Name", "Type", "Description", "CourseIdentifiers")), file=f)
            for row in rows:
                program_Identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Program/" + str(row[0])))
                OrgUnitIdentifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Org/" + str(row[1])))
                Name = row[2]
                Type = row[3]
                Description = row[4]
                CourseIdentifiers = list(map(lambda param_x:str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Course/" + str(param_x))),  row[5].split(",")))
                print(",".join((program_Identifier, OrgUnitIdentifier, Name, Type, Description, ",".join(CourseIdentifiers))), file=f)

        '''
                Enrollments
        '''
        enrollments_uri = "{0}ds/campusnexus/StudentCourses?$expand=Student($select=FirstName,LastName,EmailAddress)" \
                          "&$filter=EndDate gt {1} and StartDate le {2}" \
                          "&$select=StudentId,ClassSectionId,Status,DropDate" \
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
                             ", LastName, Email, StatusChangeDate) values (?,?,?,?,?,?,?)", (
                                 child["StudentId"],
                                 child["ClassSectionId"],
                                 child["Status"],
                                 child["Student"]["FirstName"],
                                 child["Student"]["LastName"],
                                 child["Student"]["EmailAddress"],
                                 child["DropDate"],
            )
                             )


        ""

        cur = mem_conn.cursor()
        cur.execute(
            "select PersonIdentifier, SectionIdentifier, Status, FirstName, LastName, Email, StatusChangeDate "
            "from Enrollments "
            "")
        rows = cur.fetchall()
        with open('Enrollments.csv', 'w') as f:
            print(",".join(("PersonIdentifier", "SectionIdentifier", "Status", "FirstName", "LastName", "Email", "StatusChangeDate")), file=f)
            for row in rows:
                person_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Student/" + str(row[0])))
                section_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Section/" + str(row[1])))
                status = row[2]
                first_name = row[3]
                last_name = row[4]
                email = row[5]
                statusChangeDate = row[6]
                if statusChangeDate is None:
                    status = "Active"
                    statusChangeDate = ""
                else:
                    status = "Dropped"
                print(",".join((person_identifier, section_identifier, status, first_name, last_name, email, statusChangeDate)), file=f)

            '''
                    Instructors
            '''
            instructor_uri = "{0}ds/campusnexus/StudentCourses?$expand=ClassSection($select=Id)," \
                          "ClassSection($expand=Instructor($select=StaffId)," \
                          "Instructor($expand=Staff($select=FirstName,LastName,EmailAddress,CreatedDateTime)))" \
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

                mem_conn.execute("insert into FacultyDemographics(PersonIdentifier, EffectiveOn, FirstName, LastName, EmailAddress1) values (?,?,?,?,?)", (
                    child["ClassSection"]["Instructor"]["StaffId"],
                    child["ClassSection"]["Instructor"]["Staff"]["CreatedDateTime"],
                    child["ClassSection"]["Instructor"]["Staff"]["FirstName"],
                    child["ClassSection"]["Instructor"]["Staff"]["LastName"],
                    child["ClassSection"]["Instructor"]["Staff"]["EmailAddress"],
                    )
                                 )

            cur = mem_conn.cursor()
            cur.execute(
                "select distinct PersonIdentifier, SectionIdentifier, FirstName, LastName, Email, Role "
                "from Instructors "
                "")
            rows = cur.fetchall()
            with open('Instructors.csv', 'w') as f:
                print(",".join(("PersonIdentifier", "SectionIdentifier", "FirstName", "LastName", "Email", "Role")), file=f)
                for row in rows:
                    person_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Account/" + str(row[0])))
                    section_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Section/" + str(row[1])))
                    first_name = row[2]
                    last_name = row[3]
                    email = row[4]
                    role = row[5]
                    print(",".join((person_identifier, section_identifier, first_name, last_name, email, role)), file=f)


            cur = mem_conn.cursor()
            cur.execute(
                "select distinct PersonIdentifier, EffectiveOn, FirstName, LastName, EmailAddress1 "
                "from FacultyDemographics "
                "")
            rows = cur.fetchall()
            with open('FacultyDemographics.csv', 'w') as f:
                print(",".join(("PersonIdentifier", "EffectiveOn", "FirstName", "LastName", "EmailAddress1")), file=f)
                for row in rows:
                    person_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Account/" + str(row[0])))
                    effective_on = row[1]
                    first_name = row[2]
                    last_name = row[3]
                    email = row[4]
                    print(",".join((person_identifier, effective_on, first_name, last_name, email)), file=f)

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
                print(",".join(("SectionIdentifier", "TermIdentifier", "CourseIdentifier", "Number", "BeginDate", "EndDate", "DeliveryMode")), file=f)
                for row in rows:
                    section_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Section/" + str(row[0])))
                    term_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Term/" + str(row[1])))
                    course_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Course/" + str(row[2])))
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
                print(",".join(("CourseIdentifier", "Subject", "Number", "Title", "OrgUnitIdentifier", "Type")), file=f)
                for row in rows:
                    course_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Course/" + str(row[0])))
                    subject = row[1]
                    number = row[2]
                    title = row[3]
                    org_unit_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Org/" + str(row[4])))
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
                print(",".join(("TermIdentifier", "Name", "BeginDate", "EndDate", "ParentIdentifier", "Type")), file=f)
                for row in rows:
                    term_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Term/" + str(row[0])))
                    name = row[1]
                    begin_date = row[2]
                    end_date = row[3]
                    type = row[4]
                    print(",".join((term_identifier, name, begin_date, end_date, "", type)), file=f)

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
                # print(child)

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
                    org_unit_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Org/" + str(row[0])))
                    name = row[1]
                    acronym = row[2]
                    type = row[3]
                    print(",".join((org_unit_identifier, name, acronym, type)), file=f)

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
                # print(child)

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
                print(",".join(("OrgUnitIdentifier", "Name", "Acronym", "Type")), file=f)
                for row in rows:
                    org_unit_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Org/" + str(row[0])))
                    name = row[1]
                    acronym = row[2]
                    type = row[3]
                    print(",".join((org_unit_identifier, name, acronym, type)), file=f)

            '''
                    Account Data
            '''
            #   students
            account_uri = "{0}ds/campusnexus/StudentCourses?$select=Student&$expand=Student($select=Id,FirstName,LastName,EmailAddress){3}" \
                           "&$filter=Term/EndDate gt {1} and Term/StartDate le {2}" \
                           "".format(root_uri, now.strftime("%Y-%m-%d"),
                                     (now + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"), top)

            print(account_uri)
            r = s.get(account_uri)
            r.raise_for_status()

            # result = r.json()
            result = json.loads(r.text)
            for child in result.get("value"):
                # print(child)

                mem_conn.execute("insert into AccountData(PersonIdentifier, FirstName, LastName, Email) values (?,?,?,?)", (
                    child["Student"]["Id"],
                    child["Student"]["FirstName"],
                    child["Student"]["LastName"],
                    child["Student"]["EmailAddress"],
                )
                                 )

            #   instructors
            account_uri = "{0}ds/campusnexus/StudentCourses?$expand=ClassSection($select=Instructor),ClassSection($expand=Instructor($select=Staff),Instructor($expand=Staff($select=EmailAddress,Person),Staff($expand=Person($select=LastName,FirstName,Id))))" \
                              "&$filter=EndDate gt {1} and StartDate le {2}" \
                              "&$select=ClassSection" \
                              "".format(root_uri, now.strftime("%Y-%m-%d"),
                                        (now + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))

            print(account_uri)
            r = s.get(account_uri)
            r.raise_for_status()

            # result = r.json()
            result = json.loads(r.text)
            for child in result.get("value"):
                # print(child)
                mem_conn.execute("insert into AccountData(PersonIdentifier, FirstName, LastName, Email) values (?,?,?,?)", (
                    child["ClassSection"]["Instructor"]["Staff"]["Person"]["Id"],
                    child["ClassSection"]["Instructor"]["Staff"]["Person"]["FirstName"],
                    child["ClassSection"]["Instructor"]["Staff"]["Person"]["LastName"],
                    child["ClassSection"]["Instructor"]["Staff"]["EmailAddress"],
                )
                                 )

            cur = mem_conn.cursor()
            cur.execute(
                "select distinct PersonIdentifier, FirstName, LastName, Email "
                "from AccountData "
                "")
            rows = cur.fetchall()
            with open('Accounts.csv', 'w') as f:
                print(",".join(("PersonIdentifier", "FirstName", "LastName", "Email")), file=f)
                for row in rows:
                    person_identifier = str(uuid.uuid3(uuid.NAMESPACE_URL, "//lcu.edu/Account/" + str(row[0])))
                    first_name = row[1]
                    last_name = row[2]
                    email = row[3]
                    print(",".join((person_identifier, first_name, last_name, email)), file=f)
