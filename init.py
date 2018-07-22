import json

cm = []
output_file = "cm.json"

mass = {}
mass['name'] = 'Critical Mass Darmstadt'
mass['location'] = 'Marktplatz'
mass['begin'] = '19:00'
mass['urls'] = ['https://www.instagram.com/criticalmassdarmstadt/', 'https://twitter.com/criticalmassda', 'https://de-de.facebook.com/KritischeMasseDarmstadt/']
mass['day'] = 'Friday'
mass['cycle'] = 3

cm.append(mass)

mass = {}
mass['name'] = 'Critical Mass Stuttgart'
mass['location'] = 'Feuerseeplatz'
mass['begin'] = '18:30'
mass['urls'] = ['https://criticalmassstuttgart.wordpress.com/', 'https://www.facebook.com/getonyourbike']
mass['day'] = 'Friday'
mass['cycle'] = 2

cm.append(mass)

mass = {}
mass['name'] = 'Critical Mass Würzburg'
mass['location'] = 'am Brunnen vor der Residenz'
mass['begin'] = '18:00'
mass['urls'] = ['https://www.facebook.com/Critical-Mass-W%C3%BCrzburg-638967912866066', 'http://criticalmass.de/www.cmwue.de']
mass['day'] = 'Friday'
mass['cycle'] = 3


cm.append(mass)
json.dump(cm, open(output_file, "w"))
