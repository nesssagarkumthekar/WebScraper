from Scrapers import WFGCRAWLER1 as Wf
from configs import  WFGGLOBAL as Wg

#member =[['NAOMI','RHODES'],'75225-4611']
#member =[['Pearl','Maalouf'],22201-4611]
#member = [['Matthew', 'Noble'], '43017-2950']
#member = [['Matthew','Lowe'],'75225-6330']
#member=[['Jeffrey', 'Kratz'], '76102-3105']
member =[['Jill','Bradley'],'40207-5212']

Wf.process_members(member)
print('--------------------------')
print(Wg.Url_A)
print(Wg.Group_A)
print(Wg.Des_A)
print(Wg.Phone_A)
print(Wg.Email_A)
print(Wg.Primary_A)
print(Wg.Link_A)