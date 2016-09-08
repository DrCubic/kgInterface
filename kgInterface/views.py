# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#import settings
import json
import os

# path settings for rdf3x
RDF3X_API_DIR = "/var/rdf3x/bin/"
KG_DAT_DIR = "/var/rdf3x/"
KG_DATABASE = "kgdatanew"
REQ_FILE_DIR = "/var/www/djangoapi/file/"

# setting for knowledge graph definition
PREFIX_BASE = "<http://xianjiaotong.edu/"
PREFIX_PRO = PREFIX_BASE + "property/>"
PREFIX_DIS = PREFIX_BASE + "disease/>"
PREFIX_LAB = PREFIX_BASE + "lab/>"
PREFIX_SYM = PREFIX_BASE + "symptom/>"
PREFIX_MED = PREFIX_BASE + "medicine/>"
PREFIX_DC = PREFIX_BASE + "dclass/>"
PREFIX_MC = PREFIX_BASE + "mclass/>"
PREFIX_SC = PREFIX_BASE + "sclass/>"
PREFIX_SB = PREFIX_BASE + "sbody/>"
PREFIX_LC = PREFIX_BASE + "lclass/>"

ABBRAVIATION_PRO = "pro:"
ABBRAVIATION_DIS = "dis:"
ABBRAVIATION_LAB = "lab:"
ABBRAVIATION_SYM = "sym:"
ABBRAVIATION_MED = "med:"
ABBRAVIATION_DC = "dc:"
ABBRAVIATION_MC = "mc:"
ABBRAVIATION_SC = "sc:"
ABBRAVIATION_SB = "sb:"
ABBRAVIATION_LC = "lc:"

rel_chinese_dic = {}
rel_chinese_dic["DisOtherLink"] = "其他关系"
rel_chinese_dic["DisLab"] = "实验室检查" 
rel_chinese_dic["DisOtherLab"] = "其他辅助检查"
rel_chinese_dic["DisDiag"] = "诊断"
rel_chinese_dic["DisDiagDiff"] = "鉴别诊断"
rel_chinese_dic["DisComp"] = "并发症"
rel_chinese_dic["DisMedi"] = "治疗"
rel_chinese_dic["DisProg"] = "预后"
rel_chinese_dic["DisPathogen"] = "发病机制"
rel_chinese_dic["DisManifest"] = "临床表现"
rel_chinese_dic["DisCause"] = "病因"
rel_chinese_dic["DisOver"] = "概述"
rel_chinese_dic["DisEpid"] = "流行病学"
rel_chinese_dic["DisPrecau"] = "预防"
rel_chinese_dic["Disclass"] = "科室"
rel_chinese_dic["RelateDrag"] = "相关药物"
rel_chinese_dic["RelateDis"] = "相关疾病"
rel_chinese_dic["RelateLab"] = "相关检查"

rel_chinese_dic["MedOtherLink"] = "其他关系"
rel_chinese_dic["MedIndDiag"] = "适应症"
rel_chinese_dic["MedContDiag"] = "禁忌症"
rel_chinese_dic["Med"] = "药物相互作用"
rel_chinese_dic["MedPharmaAct"] = "药理作用"
rel_chinese_dic["MedDosage"] = "药物剂型"
rel_chinese_dic["MedInstruct"] = "用法用量"
rel_chinese_dic["MedPharmacok"] = "药动学"
rel_chinese_dic["MedAtten"] = "注意事项"
rel_chinese_dic["MedRect"] = "不良反应"
rel_chinese_dic["MedOpin"] = "专家点评"
rel_chinese_dic["MedRelateDrag"] = "相关药物"
rel_chinese_dic["MedRelateDis"] = "相关疾病"
rel_chinese_dic["MedRelateLab"] = "相关检查"

rel_chinese_dic["MedFirClass"] = "一级关系"
rel_chinese_dic["MedSecClass"] = "二级关系"
rel_chinese_dic["MedThrClass"] = "三级关系"
rel_chinese_dic["McParent"] = "药物父母关系"

rel_chinese_dic["SymComCheck"] = "常用检查"
rel_chinese_dic["SymPosDis"] = "可能疾病"
rel_chinese_dic["SymFirClass"] = "一级关系"
rel_chinese_dic["SymSecClass"] = "二级关系"
rel_chinese_dic["SymFirBody"] = "一级部位"
rel_chinese_dic["SymSecBody"] = "二级部位"
rel_chinese_dic["SymOtherLink"] = "其他关系"
rel_chinese_dic["ScParent"] = "科室父母关系"
rel_chinese_dic["SbParent"] = "部位父母关系"

rel_chinese_dic["LabOtherLink"] = "其他关系"
rel_chinese_dic["LabNote"] = "附注"
rel_chinese_dic["LabOper"] = "操作方法"
rel_chinese_dic["LabClinSig"] = "临床意义"
rel_chinese_dic["LabOverview"] = "概述"
rel_chinese_dic["LabPrin"] = "原理"
rel_chinese_dic["LabReag"] = "试剂"
rel_chinese_dic["LabRelateDrag"] = "相关药物"
rel_chinese_dic["LabRelateDis"] = "相关疾病"
rel_chinese_dic["LabRelateLab"] = "相关检查"
rel_chinese_dic["LabFirClass"] = "一级关系"
rel_chinese_dic["LabSecClass"] = "二级关系"
rel_chinese_dic["LcParent"] = "检查父母关系"


class RDF_node:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        if self.type == "dis":
            self.abbraviation = ABBRAVIATION_DIS
        elif self.type == "lab":
            self.abbraviation = ABBRAVIATION_LAB
        elif self.type == "sym":
            self.abbraviation = ABBRAVIATION_SYM
        elif self.type == "med":
            self.abbraviation = ABBRAVIATION_MED
        elif self.type == "dc":
            self.abbraviation = ABBRAVIATION_DC
        elif self.type == "mc":
            self.abbraviation = ABBRAVIATION_MC
        elif self.type == "sc":
            self.abbraviation = ABBRAVIATION_SC
        elif self.type == "sb":
            self.abbraviation = ABBRAVIATION_SB
        elif self.type == "lc":
            self.abbraviation = ABBRAVIATION_LC
        elif self.type == None:
            # this serverd as a dummy node type
            self.abbraviation = None
        else:
            raise ValueError("Invalid node type for RDF.")
        prefix_str = "PREFIX " + ABBRAVIATION_PRO + PREFIX_PRO
        prefix_str += " PREFIX " + ABBRAVIATION_DIS + PREFIX_DIS
        prefix_str += " PREFIX " + ABBRAVIATION_LAB + PREFIX_LAB
        prefix_str += " PREFIX " + ABBRAVIATION_SYM + PREFIX_SYM
        prefix_str += " PREFIX " + ABBRAVIATION_MED + PREFIX_MED
        prefix_str += " PREFIX " + ABBRAVIATION_DC + PREFIX_DC
        prefix_str += " PREFIX " + ABBRAVIATION_MC + PREFIX_MC
        prefix_str += " PREFIX " + ABBRAVIATION_SC + PREFIX_SC
        prefix_str += " PREFIX " + ABBRAVIATION_SB + PREFIX_SB
        prefix_str += " PREFIX " + ABBRAVIATION_LC + PREFIX_LC
        self.prefix = prefix_str

    def query_all(self):
        '''
        Obtain all the relations and nodes that are connects (both direction)
        to the specific node
        '''
        query = self.prefix
        query += ' SELECT DISTINCT ?r ?n WHERE {{?x ?r ?n FILTER (regex (?x, "' + str(
            self.id) + '"))} UNION {?n ?r ?x FILTER (regex (?x, "' + str(
                self.id) + '"))}}'
        return query

    def get_property(self):
        '''
        This function generate the query to obtain all the property
        '''
        query = self.prefix
        query += ' SELECT DISTINCT ?r ?n WHERE { ' + self.abbraviation + self.id + ' ?r ?n FILTER (regex (?r, "property"))}'
        return query

    def get_path_one_node(self):
        '''
        This function generate the query to obtain all the 
        node (both in or out link) that connects to the query node
        The retrun result from RDF will be in the format of:
        "relationship" "id" "chinese_name"
        '''
        query = self.prefix
        query += ' SELECT DISTINCT ?r ?n ?p WHERE { ' + self.abbraviation + self.id + '?r ?n FILTER (!regex (?r, "property")). ?n pro:name ?p}'
        return query

    def get_path_one_node_cross_rel(self):
        '''
        It generates cross raltionships between all one degree node
        The returned result is in the form of 
        id1 chinese_name_1 relationship id2 chinese_name_2
        where id1 and id2 are all the belongs to (subset of) the list
        of ids that "get_path_one_node" returns
        '''
        query = self.prefix
        query += ' SELECT DISTINCT ?n1 ?p1 ?r ?n2 ?p2 WHERE { ' + self.abbraviation + self.id + ' ?r1 ?n1 FILTER (!regex (?r1, "property")).' + self.abbraviation + self.id + ' ?r2 ?n2 FILTER (!regex (?r2, "property")).' + '?n1 ?r ?n2. ?n1 pro:name ?p1. ?n2 pro:name ?p2.}'
        return query

# In[ ]:


def get_first_order_rel(id_list):
    '''
    This function is used to generate a query that returns all 
    first order relationships among a set of different nodes
    RDF returned format: 
        id1, chinese_name_1 ,relationship, id2, chinese_name_2,
    where id1 and id2 have to be in the id_list.
    '''
    # generate a dummy RDF node
    dummy_node = RDF_node(None, None)
    query = dummy_node.prefix
    query += ' SELECT DISTINCT ?n1 ?c1 ?p ?n2 ?c2 WHERE { ?n1 ?p ?n2 ' + 'FILTER (('

    # regular expression for the first node (n1 node)
    for idx, node_id in enumerate(id_list):
        node_id = str(node_id).strip()
        if idx == len(id_list) - 1:
            query += 'regex (?n1, "' + node_id + '") ) && '
        else:
            query += 'regex (?n1, "' + node_id + '") || '
    # regular expression for the second node (n2 node)
    query += '('
    for idx, node_id in enumerate(id_list):
        node_id = str(node_id).strip()
        if idx == len(id_list) - 1:
            query += 'regex (?n2, "' + node_id + '") )'
        else:
            query += 'regex (?n2, "' + node_id + '") || '
    query += ').'
    query += ' ?n1 pro:name ?c1. ?n2 pro:name ?c2.}'

    return query

# In[ ]:


def get_second_order_rel(id_list):
    '''
    This function is used to generate a query that returns all 
    second order relationships among a set of different nodes. 
    REF return format: 
        id1, chinese_name1, relationship1, connected_node_id, 
        connected_node_chinese_name, relationship2, id2, 
        chinese_name2
    where, id1 and id2 have to be in the set of id_list. 
    '''
    # generate a dummy RDF node
    dummy_node = RDF_node(None, None)
    query = dummy_node.prefix
    query += ' SELECT DISTINCT ?n1 ?c1 ?p1 ?d ?c ?p2 ?n2 ?c2 ' + 'WHERE { ?n1 ?p1 ?d. FILTER ('
    # regular expression for the first node (n1 node)
    for idx, node_id in enumerate(id_list):
        node_id = str(node_id).strip()
        if idx == len(id_list) - 1:
            query += 'regex (?n1, "' + node_id + '") ) '
        else:
            query += 'regex (?n1, "' + node_id + '") || '

    # second query expression
    query += '?d ?p2 ?n2 ' + 'FILTER ('
    # regular expression for the second node (n2 node)
    for idx, node_id in enumerate(id_list):
        node_id = str(node_id).strip()
        if idx == len(id_list) - 1:
            query += 'regex (?n2, "' + node_id + '") ).'
        else:
            query += 'regex (?n2, "' + node_id + '") || '
    query += ' ?n1 pro:name ?c1. ?n2 pro:name ?c2. ?d pro:name ?c.}'

    return query

# In[ ]:


def find_from_input(id_list, return_type):
    '''
    This function is used to retrun all disease or meds that
    are all connected with the inputs 
    Ex: input = ["s15394", "m12767", "l1087", "m12754"], 
    we want to return disease 
    '''
    if return_type == "dis":
        property_type = "disease"
    elif return_type == "med":
        property_type = "medicine"
    else:
        raise ValueError("Unsupported return type")
    abbraviation = return_type + ":"
    # generate a dummy RDF node
    dummy_node = RDF_node(None, None)
    query = dummy_node.prefix
    query += ' SELECT ?n1 ?r ?n2 WHERE {' + ' ?n1 ?r ?n2. ?n2 pro:type "' + property_type + '". FILTER ('
    for idx, node_id in enumerate(id_list):
        node_id = str(node_id).strip()
        if idx == len(id_list) - 1:
            query += 'regex (?n1, "' + node_id + '") )}'
        else:
            query += 'regex (?n1, "' + node_id + '") || '

    return query

def call_api_rdf3x(request):
    req_content = request

    tmp_file_dir = REQ_FILE_DIR
    tmp_file = tmp_file_dir + "input"
    file_obj = open(tmp_file, "w")
    file_obj.write(req_content)
    file_obj.close()

    api_dir = RDF3X_API_DIR
    dat_dir = KG_DAT_DIR
    dbname = dat_dir + KG_DATABASE
    command_line = api_dir + "rdf3xquery " + dbname + " " + tmp_file
    #print(command_line)

    api_req = os.popen(command_line)
    out_list = api_req.readlines()

    return out_list

def get_node_name(meta_data):
    metas = meta_data
    #print metas
    pre_string = "<http://xianjiaotong.edu/property/"
    if(metas[0] == "<empty result>\n"):
        return ""
    else:
        for i in range(0,len(metas)):
            meta_arr = metas[i].split(" ")
            meta_arr[0] = meta_arr[0].replace(pre_string,"")
            meta_arr[0] = meta_arr[0].replace(">","")
           
            if(meta_arr[0] == "name"):
               tname = meta_arr[1].replace("\"","")
               tname = tname.strip()
               #print tname
               return tname


def get_prefix(fid):
    first = fid[0]
    if first == 'd':
        return "dis" 
    elif first == 'l':
        return "lab"
    elif first == 'm':
        return "med"
    elif first == 's':
        return "sym"
    elif first == 'b':
        return "sbody"
    elif first == 'z':
        return "sclass"
    elif first == 'p':
        return "mclass"
    elif first == 'b':
        return "sbody"
    elif first == 'j':
        return "lclass"
    elif first == 'c':
        return "dclass"

def get_cat(cat):
    if cat == "dis":
        return "disease"
    elif cat == "lab":
        return "lab"
    elif cat == "med":
        return "medicine"
    elif cat == "sym":
        return "symptom"
    elif cat == "lclass":
        return "lclass"
    elif cat == "dclass":
        return "dclass"
    elif cat == "mclass":
        return "mclass"
    elif cat == "sclass":
        return "sclass"
    elif cat == "sbody":
        return "sbody"

def get_id(in_link):
    link = in_link.replace("\n","")
    pre_string = "<http://xianjiaotong.edu/"
    if "disease" in link:
        rem_string = pre_string + "disease/"
        link = link.replace(rem_string,"")
        link = link.replace(">","")
    elif "lab" in link:
        rem_string = pre_string + "lab/"
        link = link.replace(rem_string,"")
        link = link.replace(">","")
    elif "medicine" in link:
        rem_string = pre_string + "medicine/"
        link = link.replace(rem_string,"")
        link = link.replace(">","")
    elif "symptom" in link:
        rem_string = pre_string + "symptom/"
        link = link.replace(rem_string,"")
        link = link.replace(">","")
    elif "property" in link:
        rem_string = pre_string + "property/"
        link = link.replace(rem_string,"")
        link = link.replace(">","")
    elif "dclass" in link:
        rem_string = pre_string + "dclass/"
        link = link.replace(rem_string,"")
        link = link.replace(">","")
    elif "mclass" in link:
        rem_string = pre_string + "mclass/"
        link = link.replace(rem_string,"")
        link = link.replace(">","")
    elif "sclass" in link:
        rem_string = pre_string + "sclass/"
        link = link.replace(rem_string,"")
        link = link.replace(">","")
    elif "sbody" in link:
        rem_string = pre_string + "sbody/"
        link = link.replace(rem_string,"")
        link = link.replace(">","")
    elif "lclass" in link:
        rem_string = pre_string + "lclass/"
        link = link.replace(rem_string,"")
        link = link.replace(">","")

    return link

def get_type(fid):
    if "disease" in fid:
        return "disease" 
    elif "lab" in fid:
        return "lab"
    elif "medicine" in fid:
        return "medicine"
    elif "symptom" in fid:
        return "symptom"
    elif "sbody" in fid:
        return "sbody"
    elif "sclass" in fid:
        return "sclass"
    elif "dclass" in fid:
        return "dclass"
    elif "mclass" in fid:
        return "mclass"
    elif "lclass" in fid:
        return "lclass" 

def get_nodes_json(center,nodes_list):
    list_nodes = nodes_list
    ret_json = []
    ret_list = []
    check_list = []

    if(list_nodes[0] == "<empty result>\n"):
        return {}
    else:
        #print list_nodes
        for i in range(0,len(list_nodes)):
            data_list = {}
            data_list["data"] = {}

            data_json = {}
            data_json["data"] = {}
            node_arr = list_nodes[i].split(" ")
            node_arr[2] = node_arr[2].replace("\n","")
            
            did = get_id(node_arr[1])
            data_list["data"]["source"] = center
            data_list["data"]["target"] = did
            data_list["data"]["selected"] = "false"
            rel = rel_chinese_dic[get_id(node_arr[0])]
            data_list["data"]["relation"] = rel
            ret_list.append(data_list)

            if did not in check_list:
              check_list.append(did)

              data_json["data"]["id"] = did
              nname = node_arr[2].replace("\"","")
              data_json["data"]["name"] = nname
              data_json["data"]["type"] = get_type(node_arr[1])
              data_json["data"]["center"] = "no"
              ret_json.append(data_json)

    return ret_json,ret_list

def get_edges_json(edges_list):
    list_edges = edges_list
    ret_json = []
    check_list = []

    if(list_edges[0] == "<empty result>\n"):
        return ""
    else:
        #print len(list_edges)
        for i in range(0,len(list_edges)):
            data_json = {}
            data_json["data"] = {}
            edge_arr = list_edges[i].split(" ")
            sid = get_id(edge_arr[0])
            tid = get_id(edge_arr[3])
            rel = get_id(edge_arr[2])
            com = sid + rel + tid
            rcom = tid + rel + sid
            #print com
            if com not in check_list:
               check_list.append(com)
               check_list.append(rcom)
               data_json["data"]["source"] = sid
               data_json["data"]["target"] = tid
               data_json["data"]["selected"] = "false"
               data_json["data"]["level"] = "2"
               data_json["data"]["relation"] = rel_chinese_dic[rel]
               ret_json.append(data_json)

    return ret_json

def get_nodes_edges_json(edges_list):
    list_edges = edges_list
    #print list_edges
    ret_nodes_json = []
    ret_edges_json = []
    edge_check_list = []
    node_check_list = []

    if(list_edges[0] == "<empty result>\n"):
        return ret_nodes_json,ret_edges_json
    else:
        #print len(list_edges)
        for i in range(0,len(list_edges)):
            data_json = {}
            data_json["data"] = {}
            snode_json = {}
            snode_json["data"] = {}
            tnode_json = {}
            tnode_json["data"] = {}

            edge_arr = list_edges[i].split(" ")
            sid = get_id(edge_arr[0])
            sname = edge_arr[1]
            sname = sname.replace("\"","")
            tid = get_id(edge_arr[3])
            rel = get_id(edge_arr[2])
            tname = edge_arr[4]
            tname = tname.replace("\"","")
            com = sid + rel + tid
            rcom = tid + rel + sid

            if com not in edge_check_list:
               edge_check_list.append(com)
               edge_check_list.append(rcom)
               data_json["data"]["source"] = sid
               data_json["data"]["target"] = tid
               data_json["data"]["selected"] = "false"
               data_json["data"]["level"] = "1"
               data_json["data"]["relation"] = rel_chinese_dic[rel]
               ret_edges_json.append(data_json)

            if sid not in node_check_list:
                #print sid
                node_check_list.append(sid)
                snode_json["data"]["id"] = sid
                scat = get_prefix(sid)
                scategory = get_cat(scat)
                snode_json["data"]["type"] = scategory
                snode_json["data"]["center"] = "no"
                snode_json["data"]["name"] = sname
                #print sname
                ret_nodes_json.append(snode_json)

            if tid not in node_check_list:
                #print tid
                node_check_list.append(tid)
                tnode_json["data"]["id"] = tid
                tcat = get_prefix(tid)
                tcategory = get_cat(tcat)
                tnode_json["data"]["type"] = tcategory
                tnode_json["data"]["center"] = "no"
                tnode_json["data"]["name"] = tname
                #print tname
                ret_nodes_json.append(tnode_json)

    return ret_nodes_json,ret_edges_json

def get_nodes_list(content_list):
    list_content = content_list
    ret_list = []

    if(list_content[0] == "<empty result>\n"):
        return ret_list
    else:
        #print len(list_content)
        for i in range(0,len(list_content)):
            node_arr = list_content[i].split(" ")
            node_id = get_id(node_arr[2])

            if node_id not in ret_list:
                ret_list.append(node_id)

    return ret_list

            
@csrf_exempt
def get_node_info(request):  # get the 1-st order link information of a given node
    if request.method == "POST":
      json_out = {}
      tmp_json = {}
      tmp_json["data"] = {}
      
      try:
        json_elements = {}
        json_nodes = []
        json_edges = []

        input_dict =  json.loads(request.body)
        nid = input_dict["NID"]
        cat = get_prefix(nid)
        category = get_cat(cat)
        a = RDF_node(nid,cat)
        ret_nodes_query = a.get_path_one_node()
        #print ret_nodes_query
        out_nodes = call_api_rdf3x(ret_nodes_query)
        #print out_nodes
        (json_nodes,ret_edges) = get_nodes_json(nid,out_nodes)
        #print json_nodes
        #print ret_edges
        ret_name_query = a.get_property()
        out_meta = call_api_rdf3x(ret_name_query)

        tmp_json["data"]["id"] = nid
        tmp_json["data"]["type"] = category
        tmp_json["data"]["center"] = "yes"
        tmp_json["data"]["name"] = get_node_name(out_meta)
        json_nodes.append(tmp_json)        

        ret_edges_query = a.get_path_one_node_cross_rel()
        out_edges = call_api_rdf3x(ret_edges_query)
        json_edges = get_edges_json(out_edges)

        #print len(json_edges)
        if json_edges == "":
            json_edges = ret_edges
        else:
            json_edges = json_edges + ret_edges

        json_elements["nodes"] = json_nodes
        json_elements["edges"] = json_edges
        json_out["elements"] = json_elements

        json_out["return"] = 0

      except:
        json_out["return"] = 1
        json_out["elements"] = {}

      return HttpResponse(json.dumps(json_out), content_type="application/json")

@csrf_exempt
def get_diseases_relations(request):  # get disease list back
    if request.method == "POST":
      json_out = {}
      try:
        json_element = {}
        json_nodes = []
        json_edges = []
        input_dict = json.loads(request.body)
        id_list = input_dict["DIDS"]
        id_size = len(id_list)

        if (id_size<=5):
           ret_first_query = get_first_order_rel(id_list)
           ret_second_query = get_second_order_rel(id_list)
        else:
           ret_first_query = get_first_order_rel(id_list)
           sub_list = id_list[0:5]
           ret_second_query = get_second_order_rel(sub_list)
        
        out_first_edges = call_api_rdf3x(ret_first_query)
        out_second_edges = call_api_rdf3x(ret_second_query)

        if (out_first_edges[0] == "<empty result>\n"):
           out_edges = out_second_edges
        else:
           out_edges = out_first_edges + out_second_edges
        
        (json_nodes,json_edges) = get_nodes_edges_json(out_edges)

        json_out["nodes"] = json_nodes
        json_out["edges"] = json_edges
        json_out["return"] = 0

      except:
        json_out["nodes"] = []
        json_out["return"] = 1
        json_out["edges"] = []

      return HttpResponse(json.dumps(json_out), content_type="application/json")

@csrf_exempt
def get_medicines_relations(request):  # get disease list back
    if request.method == "POST":
      json_out = {}
      try:
        json_elements = {}
        json_nodes = []
        json_edges = []
        input_dict = json.loads(request.body)
        id_list = input_dict["MIDS"]
        id_size = len(id_list)

        if (id_size<=5):
           ret_first_query = get_first_order_rel(id_list)
           ret_second_query = get_second_order_rel(id_list)
        else:
           ret_first_query = get_first_order_rel(id_list)
           sub_list = id_list[0:5]
           ret_second_query = get_second_order_rel(sub_list)

        out_first_edges = call_api_rdf3x(ret_first_query)
        out_second_edges = call_api_rdf3x(ret_second_query)

        if (out_first_edges[0] == "<empty result>\n"):
           out_edges = out_second_edges
        else:
           out_edges = out_first_edges + out_second_edges

        (json_nodes,json_edges) = get_nodes_edges_json(out_edges)

        json_out["nodes"] = json_nodes
        json_out["edges"] = json_edges
        json_out["return"] = 0

      except:
        json_out["nodes"] = []
        json_out["return"] = 1
        json_out["edges"] = []

      return HttpResponse(json.dumps(json_out), content_type="application/json")


@csrf_exempt
def get_diseases_out(request):  # get disease list back
    if request.method == "POST":
      json_out = {}
      try:
        json_elements = []
        id_list = []
        return_type = "dis"
        input_dict = json.loads(request.body)        

        for key in input_dict.keys():
            tmp_list = input_dict[key]
            for ele in tmp_list:
                id_list.append(ele)

        ret_query = find_from_input(id_list,return_type)
        out_nodes = call_api_rdf3x(ret_query)
        json_elements = get_nodes_list(out_nodes)

        json_out["elements"] = json_elements
        json_out["return"] = 0

      except:
        json_out["return"] = 1
        json_out["elements"] = []

      return HttpResponse(json.dumps(json_out), content_type="application/json")

@csrf_exempt
def get_diseases_out_v2(request):  # get disease list back
    if request.method == "POST":
      json_out = {}
      try:
        json_elements = []
        and_list = []
        not_list = []
        remove_list = []
        return_type = "dis"
     
        input_dict = json.loads(request.body)
        and_list = input_dict["AND"]
        not_list = input_dict["NOT"]

        and_query = find_from_input(and_list,return_type)
        and_nodes = call_api_rdf3x(and_query)
        and_nodes = get_nodes_list(and_nodes)
        not_query = find_from_input(not_list,return_type)
        not_nodes = call_api_rdf3x(and_query)
        not_nodes = get_nodes_list(not_nodes)

        print not_list
        print and_list
        out_nodes = []
        for nid in and_nodes:
            if nid not in not_nodes:
                out_nodes.append(nid)
        
        #print len(out_nodes)
        if len(out_nodes) == 0:
            out_nodes = and_nodes
            remove_list = not_list

        json_out["elements"] = out_nodes
        json_out["return"] = 0
        json_out["remove"] = remove_list

      except:
        json_out["return"] = 1
        json_out["elements"] = []
        json_out["remove"] = []

      return HttpResponse(json.dumps(json_out), content_type="application/json")

@csrf_exempt
def get_medicines_out(request):  # get disease list back
    if request.method == "POST":
      json_out = {}
      try:
        json_elements = []
        and_list = []
        not_list = []
        remove_list = []
        return_type = "dis"
     
        input_dict = json.loads(request.body)
        and_list = input_dict["AND"]
        not_list = input_dict["NOT"]

        and_query = find_from_input(and_list,return_type)
        and_nodes = call_api_rdf3x(ret_query)
        and_nodes = get_nodes_list(and_nodes)
        not_query = find_from_input(not_list,return_type)
        not_nodes = call_api_rdf3x(ret_query)
        not_nodes = get_nodes_list(not_nodes)

        out_nodes = []
        for nid in and_nodes:
            if nid not in not_nodes:
                out_nodes.append(nid)

        if len(out_nodes) == 0:
            out_nodes = and_nodes
            remove_list = not_list

        json_out["elements"] = out_nodes
        json_out["return"] = 0
        json_out["remove"] = remove_list

      except:
        json_out["return"] = 1
        json_out["elements"] = []
        json_out["remove"] = []

      return HttpResponse(json.dumps(json_out), content_type="application/json")

@csrf_exempt
def get_medicines_out_v2(request):  # get disease list back
    if request.method == "POST":
      json_out = {}
      try:
        json_elements = []
        and_list = []
        not_list = []
        remove_list = []
        return_type = "med"
     
        input_dict = json.loads(request.body)
        and_list = input_dict["AND"]
        not_list = input_dict["NOT"]

        and_query = find_from_input(and_list,return_type)
        and_nodes = call_api_rdf3x(and_query)
        and_nodes = get_nodes_list(and_nodes)
        not_query = find_from_input(not_list,return_type)
        not_nodes = call_api_rdf3x(not_query)
        #print not_nodes
        not_nodes = get_nodes_list(not_nodes)

        out_nodes = []
        for nid in and_nodes:
            if nid not in not_nodes:
                out_nodes.append(nid)

        if len(out_nodes) == 0:
            out_nodes = and_nodes
            remove_list = not_list

        json_out["elements"] = out_nodes
        json_out["return"] = 0
        json_out["remove"] = remove_list

      except:
        json_out["return"] = 1
        json_out["elements"] = []
        json_out["remove"] = []

      return HttpResponse(json.dumps(json_out), content_type="application/json")
