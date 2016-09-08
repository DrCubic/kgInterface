from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
from datetime import datetime
from testapi.models import Disease,Symptom,Lab,Medication,Image
from pyweed import WeedFS
from StringIO import StringIO
import string
import random
import msgpack

useless_list = ["",u"",None,False," "]
#w = WeedFS("192.168.190.11",9333)
w = WeedFS("127.0.0.1",9333)

#disease::
#===============================================================================
database_disease_list=["Did", "Name", "Ename",  "Oname", "Dclass", "Icd10","Icd9"]
display_disease_list=["Did", "Name", "Ename",  "Oname", "Dclass", "Icd10"]
all_disease_list=["Did", "Name", "Ename",  "Oname", "Dclass", "Icd10","Icd9","Gs","Lxbx","By","Fbjz","Lcbx","Bfz","Sysjc","Qtfzjc","Zd","Zxzd","Jbzd","Zl","Yh","Yf"]
#===============================================================================
#symptom::
#===============================================================================
database_symptom_list=["Sid", "Name", "Yjks", "Ejks", "Yjbw", "Ejbw"]
display_symptom_list=["Sid", "Name", "Yjks", "Ejks", "Yjbw", "Ejbw"]
all_symptom_list=["Sid", "Name", "Yjks", "Ejks", "Yjbw", "Ejbw","Dzyp","Zs","Zzxs","Zzqy","Cyjc","Knjb","Xszz"]
#===============================================================================
#medication::
#===============================================================================
database_medication_list=["Mid", "Name", "Ename", "Oname", "Fclass", "Sclass","Tclass"]
display_medication_list=["Mid", "Name", "Ename", "Oname"]
all_medication_list=["Mid", "Name", "Ename", "Oname", "Fclass", "Sclass","Tclass","Ylzy","Yfyl","Ydx","Zysx","Zjdp","Ywxyzy","Jjz","Syz","Ywjx","Blfy"]
#===============================================================================
#lab::
#===============================================================================
database_lab_list=["Lid", "Name", "Ename", "Oname", "Fclass", "Sclass"]
display_lab_list=["Lid", "Name", "Ename", "Oname"]
all_lab_list=["Lid", "Name", "Ename", "Oname", "Fclass", "Sclass","Yl","Sj","Zcz","Lcyy","Czff","Gs","Fz"]
#===============================================================================

@csrf_exempt
def image_op(request): 
    if request.method == "POST":
        json_out = {}
        try:
            input_dict = msgpack.loads(request.body) 
            image_info = Image.objects.filter(Iid=input_dict["Iid"])
            if image_info:
                print input_dict["Iid"],'existed'
                json_out["Return"] = 1
                json_out["Results"] = 'id  exists'
            else:
                n = Image()
                nid=input_dict['Iid']
                nname=input_dict['Name']
                file2write = StringIO()
                cont =input_dict['Content']
                file2write.write(cont)
                fid = w.upload_file(None,file2write.getvalue(),'image') 
                n.Iid = nid
                n.Fid  = fid 
                n.Iname  = nname 
                n.save()
                json_out["Return"] = 0 
        except:
            traceback.print_exc()
            json_out["Return"] = 1
        return HttpResponse(json.dumps(json_out),content_type="application/json") 
    elif request.method == "DELETE":
        json_out = {}
        try: 
            input_dict = msgpack.loads(request.body) 
            image_info = Image.objects.filter(Iid=input_dict["Iid"])
            if image_info:
                n = image_info[0]
                nid=input_dict['Iid']
                w.delete_file(n.Fid) 
                n.delete()
                json_out["Return"] = 0   
            else:
                print input_dict["Iid"],'doesn\'t existed'
                json_out["Return"] = 1
                json_out["Results"] = 'id  doesn\'t exist'
        except:
            traceback.print_exc()
            json_out["Return"] = 1
        return HttpResponse(json.dumps(json_out),content_type="application/json") 

@csrf_exempt
def disease_op(request):
    if request.method == "GET":
        json_out = {}
        try:
            input_dict = json.loads(request.GET["q"]) 
            if input_dict['Table']=='Image':
                input_dict.pop('Table')
                image_info = Image.objects.get(Iid=input_dict['Iid']) 
                fid = image_info.Fid
                img = w.get_file(fid)
                response = HttpResponse(img,content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment;filename='+image_info.Iid+'.jpg' 
                return response 
            elif input_dict['Table']=='Disease':
                input_dict.pop('Table')
                json_content={}
                disease_info = Disease.objects.filter(Did=input_dict["Did"])
                if disease_info:
                    disease_info = disease_info.values()[0]
                    for key in disease_info.keys():
                        if disease_info[key] not in useless_list:
                            if key == 'id':
                                continue
                            elif key in database_disease_list:
                                #if disease_info[key]:
                                json_content[key] = disease_info[key]
                            else:
                                if disease_info[key]: 
                                    json_content[key] = w.get_file(disease_info[key])
                    json_out["Results"]=json_content
                    json_out["Return"] = 0
                else:
                    json_out["Return"] = 1
                    json_out["Results"] = 'id doesn\'t exist'
            elif input_dict['Table']=='Lab':
                input_dict.pop('Table')
                json_content={}
                lab_info = Lab.objects.filter(Lid=input_dict["Lid"])
                if lab_info:
                    lab_info = lab_info.values()[0]
                    for key in lab_info.keys():
                        if lab_info[key] not in useless_list:
                            if key == 'id':
                                continue
                            elif key in database_lab_list:
                                #if lab_info[key]:
                                json_content[key] = lab_info[key]
                            else:
                                if lab_info[key]: 
                                    json_content[key] = w.get_file(lab_info[key])
                    json_out["Results"]=json_content
                    json_out["Return"] = 0
                else:
                    json_out["Return"] = 1
                    json_out["Results"] = 'id doesn\'t exist'
            elif input_dict['Table']=='Medication':
                input_dict.pop('Table')
                json_content={}
                medication_info = Medication.objects.filter(Mid=input_dict["Mid"])
                if medication_info:
                    medication_info = medication_info.values()[0]
                    for key in medication_info.keys():
                        if medication_info[key] not in useless_list:
                            if key == 'id':
                                continue
                            elif key in database_medication_list:
                                #if medication_info[key]:
                                json_content[key] = medication_info[key]
                            else:
                                if medication_info[key]: 
                                    json_content[key] = w.get_file(medication_info[key])
                    json_out["Results"]=json_content
                    json_out["Return"] = 0
                else:
                    json_out["Return"] = 1
                    json_out["Results"] = 'id doesn\'t exist'
            elif input_dict['Table']=='Symptom':
                input_dict.pop('Table')
                json_content={}
                symptom_info = Symptom.objects.filter(Sid=input_dict["Sid"])
                if symptom_info:
                    symptom_info = symptom_info.values()[0]
                    for key in symptom_info.keys():
                        if symptom_info[key] not in useless_list:
                            if key == 'id':
                                continue
                            elif key in database_symptom_list:
                                #if symptom_info[key]:
                                json_content[key] = symptom_info[key]
                            else:
                                if symptom_info[key]: 
                                    json_content[key] = w.get_file(symptom_info[key])
                    json_out["Results"]=json_content
                    json_out["Return"] = 0
                else:
                    json_out["Return"] = 1
                    json_out["Results"] = 'id doesn\'t exist'
        except:
            traceback.print_exc()
            json_out["Return"] = 1
        return HttpResponse(json.dumps(json_out),content_type="application/json")
    elif request.method == "POST":
        json_out = {}
        try:
            input_dict = json.loads(request.body)
            if input_dict['Table']=='Disease':
                input_dict.pop('Table')
                disease_info = Disease.objects.filter(Did=json.loads(input_dict['Did']))
                if disease_info:
                    print json.loads(input_dict['Did']),'id existed'
                    json_out["Return"] = 1
                    json_out["Results"] = 'id exists'
                else:
                    n = Disease()
                    for key in input_dict: 
                        if key in database_disease_list:
                            # insert in database
                            value=json.loads(input_dict[key])
                            if type(value) is  list:
                                value=input_dict[key]
                            setattr(n,key,value) 
                        elif key in all_disease_list:
                            # insert in seaweed
                            file2write = StringIO() 
                            file2write.write(input_dict[key].encode('utf-8')) 
                            fid = w.upload_file(None,file2write.getvalue(),input_dict['Did']+'_'+key)
                            file2write.close()
                            setattr(n,key,fid)
                        else:
                            print 'keyerror',key,'not in disease'  
                    n.save()
                    json_out["Return"] = 0
            elif input_dict['Table']=='Lab':
                input_dict.pop('Table')
                lab_info = Lab.objects.filter(Lid=json.loads(input_dict['Lid']))
                if lab_info:
                    print json.loads(input_dict['Lid']),'id existed'
                    json_out["Return"] = 1
                    json_out["Results"] = 'id exists'
                else:
                    n = Lab()
                    for key in input_dict: 
                        if key in database_lab_list:
                            # insert in database
                            value=json.loads(input_dict[key])
                            if type(value) is  list:
                                value=input_dict[key]
                            setattr(n,key,value) 
                        elif key in all_lab_list:
                            # insert in seaweed
                            file2write = StringIO() 
                            file2write.write(input_dict[key].encode('utf-8')) 
                            fid = w.upload_file(None,file2write.getvalue(),input_dict['Lid']+'_'+key)
                            file2write.close()
                            setattr(n,key,fid)
                        else:
                            print 'keyerror',key,'not in lab'  
                    n.save()
                    json_out["Return"] = 0
            elif input_dict['Table']=='Medication':
                input_dict.pop('Table')
                medication_info = Medication.objects.filter(Mid=json.loads(input_dict['Mid']))
                if medication_info:
                    print json.loads(input_dict['Mid']),'id existed'
                    json_out["Return"] = 1
                    json_out["Results"] = 'id exists'
                else:
                    n = Medication()
                    for key in input_dict: 
                        if key in database_medication_list:
                            # insert in database
                            value=json.loads(input_dict[key])
                            if type(value) is  list:
                                value=input_dict[key]
                            setattr(n,key,value) 
                        elif key in all_medication_list:
                            # insert in seaweed
                            file2write = StringIO() 
                            file2write.write(input_dict[key].encode('utf-8')) 
                            fid = w.upload_file(None,file2write.getvalue(),input_dict['Mid']+'_'+key)
                            file2write.close()
                            setattr(n,key,fid)
                        else:
                            print 'keyerror',key,'not in medication'  
                    n.save()
                    json_out["Return"] = 0
            elif input_dict['Table']=='Symptom':
                input_dict.pop('Table')
                symptom_info = Symptom.objects.filter(Sid=json.loads(input_dict['Sid']))
                if symptom_info:
                    print json.loads(input_dict['Sid']),'id existed'
                    json_out["Return"] = 1
                    json_out["Results"] = 'id exists'
                else:
                    n = Symptom()
                    for key in input_dict: 
                        if key in database_symptom_list:
                            # insert in database
                            value=json.loads(input_dict[key])
                            if type(value) is  list:
                                value=input_dict[key]
                            setattr(n,key,value) 
                        elif key in all_symptom_list:
                            # insert in seaweed
                            file2write = StringIO() 
                            file2write.write(input_dict[key].encode('utf-8')) 
                            fid = w.upload_file(None,file2write.getvalue(),input_dict['Sid']+'_'+key)
                            file2write.close()
                            setattr(n,key,fid)
                        else:
                            print 'keyerror',key,'not in symptom'  
                    n.save()
                    json_out["Return"] = 0
        except:
            traceback.print_exc()
            json_out["Return"] = 1
        return HttpResponse(json.dumps(json_out),content_type="application/json")
    elif request.method == "PUT":
        json_out = {}
        try:
            input_dict = json.loads(request.body) 
            if input_dict['Table']=='Disease':
                input_dict.pop('Table')
                nid=json.loads(input_dict['Did'])
                input_dict.pop("Did")
                disease_info = Disease.objects.filter(Did=nid)
                if disease_info:
                    n=disease_info[0]
                    for key in input_dict: 
                        if key in database_disease_list:
                            # insert in database
                            value=json.loads(input_dict[key])
                            if type(value) is  list:
                                value=input_dict[key].encode('utf-8')
                            setattr(n,key,value) 
                        elif key in all_disease_list:
                            #delete from seaweed
                            fid=getattr(n,key)
                            w.delete_file(fid)
                            #insert in seaweed
                            file2write = StringIO() 
                            file2write.write(input_dict[key].encode('utf-8')) 
                            fid = w.upload_file(None,file2write.getvalue(),nid)
                            file2write.close()
                            setattr(n,key,fid)
                        else:
                            print 'keyerror',key,'not in disease'  
                    n.save()
                    json_out["Return"] = 0
                else:
                    print nid,'id doesn\'t existed'
                    json_out["Return"] = 1
                    json_out["Results"] = 'id doesn\'t exist'
            elif input_dict['Table']=='Lab':
                input_dict.pop('Table')
                nid=json.loads(input_dict['Lid'])
                input_dict.pop("Lid")
                lab_info = Lab.objects.filter(Lid=nid)
                if lab_info:
                    n=lab_info[0]
                    for key in input_dict: 
                        if key in database_lab_list:
                            # insert in database
                            value=json.loads(input_dict[key])
                            if type(value) is  list:
                                value=input_dict[key].encode('utf-8')
                            setattr(n,key,value) 
                        elif key in all_lab_list:
                            #delete from seaweed
                            fid=getattr(n,key)
                            w.delete_file(fid)
                            #insert in seaweed
                            file2write = StringIO() 
                            file2write.write(input_dict[key].encode('utf-8')) 
                            fid = w.upload_file(None,file2write.getvalue(),nid)
                            file2write.close()
                            setattr(n,key,fid)
                        else:
                            print 'keyerror',key,'not in lab'  
                    n.save()
                    json_out["Return"] = 0
                else:
                    print nid,'id doesn\'t existed'
                    json_out["Return"] = 1
                    json_out["Results"] = 'id doesn\'t exist'
            elif input_dict['Table']=='Medication':
                input_dict.pop('Table')
                nid=json.loads(input_dict['Mid'])
                input_dict.pop("Mid")
                medication_info = Medication.objects.filter(Mid=nid)
                if medication_info:
                    n=medication_info[0]
                    for key in input_dict: 
                        if key in database_medication_list:
                            # insert in database
                            value=json.loads(input_dict[key])
                            if type(value) is  list:
                                value=input_dict[key].encode('utf-8')
                            setattr(n,key,value) 
                        elif key in all_medication_list:
                            #delete from seaweed
                            fid=getattr(n,key)
                            w.delete_file(fid)
                            #insert in seaweed
                            file2write = StringIO() 
                            file2write.write(input_dict[key].encode('utf-8')) 
                            fid = w.upload_file(None,file2write.getvalue(),nid)
                            file2write.close()
                            setattr(n,key,fid)
                        else:
                            print 'keyerror',key,'not in medication'  
                    n.save()
                    json_out["Return"] = 0
                else:
                    print nid,'id doesn\'t existed'
                    json_out["Return"] = 1
                    json_out["Results"] = 'id doesn\'t exist'
            elif input_dict['Table']=='Symptom':
                input_dict.pop('Table')
                nid=json.loads(input_dict['Sid'])
                input_dict.pop("Sid")
                symptom_info = Symptom.objects.filter(Sid=nid)
                if symptom_info:
                    n=symptom_info[0]
                    for key in input_dict: 
                        if key in database_symptom_list:
                            # insert in database
                            value=json.loads(input_dict[key])
                            if type(value) is  list:
                                value=input_dict[key].encode('utf-8')
                            setattr(n,key,value) 
                        elif key in all_symptom_list:
                            #delete from seaweed
                            fid=getattr(n,key)
                            w.delete_file(fid)
                            #insert in seaweed
                            file2write = StringIO() 
                            file2write.write(input_dict[key].encode('utf-8')) 
                            fid = w.upload_file(None,file2write.getvalue(),nid)
                            file2write.close()
                            setattr(n,key,fid)
                        else:
                            print 'keyerror',key,'not in symptom'  
                    n.save()
                    json_out["Return"] = 0
                else:
                    print nid,'id doesn\'t existed'
                    json_out["Return"] = 1
                    json_out["Results"] = 'id doesn\'t exist'
        except:
            traceback.print_exc()
            json_out["Return"] = 1
        return HttpResponse(json.dumps(json_out),content_type="application/json")
    elif request.method == "DELETE":
        json_out = {}
        try: 
            input_dict = json.loads(request.body)    
            if input_dict['Table']=='Disease':
                input_dict.pop('Table')
                disease_info = Disease.objects.filter(Did=input_dict["Did"])
                if disease_info:
                    dis_info = disease_info.values()[0]
                    #####################################
                    for key in dis_info.keys():
                        if key=='id':
                            continue
                        elif key not in database_disease_list:
                            if dis_info[key] :
                                #print w.get_file(dis_info[key])
                                w.delete_file(dis_info[key])
                                #print w.get_file(dis_info[key])
                    disease_info[0].delete()
                    json_out["Return"] = 0
                else:
                    json_out["Return"] = 1
                    json_out["Results"] = 'id doesn\'t exist'
            elif input_dict['Table']=='Lab':
                input_dict.pop('Table')
                lab_info = Lab.objects.filter(Lid=input_dict["Lid"])
                if lab_info:
                    dis_info = lab_info.values()[0]
                    #####################################
                    for key in dis_info.keys():
                        if key=='id':
                            continue
                        elif key not in database_lab_list:
                            if dis_info[key] :
                                w.delete_file(dis_info[key])
                    lab_info[0].delete()
                    json_out["Return"] = 0
                else:
                    json_out["Return"] = 1
                    json_out["Results"] = 'id doesn\'t exist'
            elif input_dict['Table']=='Medication':
                input_dict.pop('Table')
                medication_info = Medication.objects.filter(Mid=input_dict["Mid"])
                if medication_info:
                    dis_info = medication_info.values()[0]
                    #####################################
                    for key in dis_info.keys():
                        if key=='id':
                            continue
                        elif key not in database_medication_list:
                            if dis_info[key] :
                                w.delete_file(dis_info[key])
                    medication_info[0].delete()
                    json_out["Return"] = 0
                else:
                    json_out["Return"] = 1
                    json_out["Results"] = 'id doesn\'t exist'
            elif input_dict['Table']=='Symptom':
                input_dict.pop('Table')
                symptom_info = Symptom.objects.filter(Sid=input_dict["Sid"])
                if symptom_info:
                    dis_info = symptom_info.values()[0]
                    #####################################
                    for key in dis_info.keys():
                        if key=='id':
                            continue
                        elif key not in database_symptom_list:
                            if dis_info[key] :
                                w.delete_file(dis_info[key])
                    symptom_info[0].delete()
                    json_out["Return"] = 0
                else:
                    json_out["Return"] = 1
                    json_out["Results"] = 'id doesn\'t exist'
        except:
            traceback.print_exc()
            json_out["Return"] = 1
        return HttpResponse(json.dumps(json_out),content_type="application/json") 

@csrf_exempt
def disease_list(request):
    if request.method == "GET": 
        json_out = {}
        try:       
            input_dict = json.loads(request.GET["q"])   
            if input_dict['Table']=='Image':          
                start_point = input_dict["Start"]
                end_point = input_dict["End"]            
                id_count = Image.objects.count()
                #####
                images = Image.objects.order_by("Iid")[start_point:min(id_count,end_point)].values()
                results = []
                for image_info in images:
                    record_list = []
                    record_list.append(image_info['Iid'])
                    record_list.append(image_info['Fid'])
                    record_list.append(image_info['Iname'])
                    results.append(record_list)
                #####
                json_out["Results"] = results
                json_out["Return"] = 0
                json_out["Total_Image_Count"] = id_count
                json_out["Image_Count"] = len(json_out["Results"])
            elif input_dict['Table']=='Disease':
                start_point = input_dict["Start"]
                end_point = input_dict["End"]            
                id_count = Disease.objects.count()
                #####
                diseases = Disease.objects.order_by("Did")[start_point:min(id_count,end_point)].values()
                results = []
                for disease_info in diseases:
                    record_list = []
                    for key in display_disease_list:
                        record_list.append(disease_info[key])
                    results.append(record_list)
                #####
                json_out["Results"] = results
                json_out["Return"] = 0
                json_out["Total_Disease_Count"] = id_count
                json_out["Disease_Count"] = len(json_out["Results"])
            elif input_dict['Table']=='Lab':
                start_point = input_dict["Start"]
                end_point = input_dict["End"]            
                id_count = Lab.objects.count()
                #####
                labs = Lab.objects.order_by("Lid")[start_point:min(id_count,end_point)].values()
                results = []
                for lab_info in labs:
                    record_list = []
                    for key in display_lab_list:
                        record_list.append(lab_info[key])
                    results.append(record_list)
                #####
                json_out["Results"] = results
                json_out["Return"] = 0
                json_out["Total_Lab_Count"] = id_count
                json_out["Lab_Count"] = len(json_out["Results"])
            elif input_dict['Table']=='Medication':
                start_point = input_dict["Start"]
                end_point = input_dict["End"]            
                id_count = Medication.objects.count()
                #####
                medications = Medication.objects.order_by("Mid")[start_point:min(id_count,end_point)].values()
                results = []
                for medication_info in medications:
                    record_list = []
                    for key in display_medication_list:
                        record_list.append(medication_info[key])
                    results.append(record_list)
                #####
                json_out["Results"] = results
                json_out["Return"] = 0
                json_out["Total_Medication_Count"] = id_count
                json_out["Medication_Count"] = len(json_out["Results"])
            elif input_dict['Table']=='Symptom':
                start_point = input_dict["Start"]
                end_point = input_dict["End"]            
                id_count = Symptom.objects.count()
                #####
                symptoms = Symptom.objects.order_by("Sid")[start_point:min(id_count,end_point)].values()
                results = []
                for symptom_info in symptoms:
                    record_list = []
                    for key in display_symptom_list:
                        record_list.append(symptom_info[key])
                    results.append(record_list)
                #####
                json_out["Results"] = results
                json_out["Return"] = 0
                json_out["Total_Symptom_Count"] = id_count
                json_out["Symptom_Count"] = len(json_out["Results"])
        except: 
            traceback.print_exc()
            json_out["Return"] = 1
        return HttpResponse(json.dumps(json_out),content_type="application/json") 
