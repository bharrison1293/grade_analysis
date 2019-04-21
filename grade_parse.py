import PyPDF2, re
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
#pdfFileObj=open('grd20181EN.pdf','rb')
#pdfReader=PyPDF2.PdfFileReader(pdfFileObj)
#files=['grd20131EN.pdf','grd20132EN.pdf','grd20133EN.pdf','grd20141EN.pdf',
#       'grd20142EN.pdf','grd20143EN.pdf','grd20151EN.pdf','grd20152EN.pdf',
#       'grd20153EN.pdf','grd20161EN.pdf','grd20162EN.pdf','grd20163EN.pdf',
#       'grd20171EN.pdf','grd20172EN.pdf','grd20173EN.pdf','grd20181EN.pdf']
#files=['grd20161EN.pdf','grd20162EN.pdf','grd20163EN.pdf',
#       'grd20171EN.pdf','grd20172EN.pdf','grd20173EN.pdf','grd20181EN.pdf']
#files=['grd20173EN.pdf','grd20181EN.pdf']
files=['grd20161EN.pdf']
#files=['grd20173EN.pdf']
courses={}
pages=''
for file in files:
# %% Collect data from files
    Term=file[3:8]
    pdfFileObj=open(file,'rb')
    pdfReader=PyPDF2.PdfFileReader(pdfFileObj)
    
    for i in range(0,pdfReader.getNumPages()):
        pages=pages+pdfReader.getPage(i).extractText()
        
    pages=pages.replace('\n','')
    REGEX = '([A-Z]{4}-\d{3})'
    ELE_TO_IGNORE = ['GRADE DISTRIBUTION']
# %% Cleanup data   
    # Split String When Encountering Major and Class Number, Ex: AERO-101
    pages = re.split(REGEX,pages)
    page_iter=iter(pages)
    page_split =[]
    for element in page_iter:
        if any(ELE in element for ELE in ELE_TO_IGNORE):
            continue
        elif re.match(REGEX,element):
            current_element=element
            next_element=next(page_iter)
            # Eliminate Special Cases of Unwanted Data
            next_element=next_element.split('COURSE TOTAL')[0] # Remove Course Total from data
            next_element=next_element.split('SECTION TEXAS A&M UNI')[0] # Remove Headers Hanging onto element ends
            next_element= ' '.join(re.split('(100.00%)',next_element)) # Seperate Occurence of 100% stuck to char
            
            # Seperate Occurences of Class Count touching professor name
            prof_count_split = ' '.join(re.split('([A-Z]+)',re.split('(\d+[A-Z]+)',next_element)[1])[0:-1])
            temp_split = re.split('(\d+[A-Z]+)',next_element)
            next_element = ' '.join([temp_split[0],prof_count_split,temp_split[-1]])
            
            page_split.append(current_element+next_element)
        else:
            element=element.split('COURSE TOTAL')[0]
            element=element.split('SECTION TEXAS A&M UNI')[0]
            page_split.append(element)

# %% Use Cleaned Data to create variables    
for line in page_split:
    j=line.split()
    course=Term+'-'+j[0]
    A=j[2]; B=j[4]; C=j[6]; D=j[8]; F=j[10]; GPA=j[11][-5:]
    a = int(j[1]); b = int(j[3]); c =int(j[5]); d = int(j[7]); f = int(j[9]);
    Q = int(j[15])
    
    # Get Professor Name and Class Count
    Prof = ''
    for element in reversed(j):
        if element.isdigit():
            count = element
            break
        else:
            Prof +=' '+element
    Prof = Prof.strip()            

    courses[course]={}
    courses[course]['Major']=j[0][:4]
    courses[course]['Term']=Term
    courses[course]['A']=A
    courses[course]['B']=B
    courses[course]['C']=C
    courses[course]['D']=D
    courses[course]['F']=F
    courses[course]['a']=a
    courses[course]['b']=b
    courses[course]['c']=c
    courses[course]['d']=d
    courses[course]['f']=f
    courses[course]['GPA']=float(GPA)
    courses[course]['Count']=count
    courses[course]['Prof']=Prof
    courses[course]['Q']=Q
df=pd.DataFrame.from_dict(courses,orient='index')

# %% Plot Stuff
#plt.figure(figsize=(12,4)) 
#fig = sns.countplot(df['Major'], data=df)
#fig.figure.savefig('major_size.png',dpi=400)
#
#majors=df['Major'].tolist()
#majors=list(set(majors))
#major_gpa={}
#for major in majors:
#    major_gpa[major]=df[df['Major']==major]['GPA'].median()
#df2=pd.DataFrame.from_dict(major_gpa, orient='index')
#plt.figure(figsize=(12,4)) 
#fig = sns.barplot(x=df2.index,y=0, data=df2)
#fig.figure.savefig('major_gpa.png',dpi=400)
