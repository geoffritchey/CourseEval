
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

create table Remove Instructor (
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
