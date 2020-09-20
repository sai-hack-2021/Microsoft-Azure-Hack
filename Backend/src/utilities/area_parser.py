import json
import os

class areas:

    with open(os.getcwd() + "/utilities/area.json", 'r') as ff:
        data = json.load(ff)

    def __int__(self):

        pass


    def get_areas(self):

        final = []

        for i in areas.data:

            final.append({"area_id":int(i),"area_name":areas.data[i]['Area_name'],"cluster_name":areas.data[i]['Cluster_name']})

        return final


    def get_stats(self,area_id):

        return areas.data[area_id]['Statistics']


    def get_appointment(self,area_id,type):


        return areas.data[area_id]['Appointments'][type]



