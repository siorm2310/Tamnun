import json 
import numpy as np 
import scipy
import matplotlib as mpl 


def Exist(item,itemlist):
    '''
    This function checks if the input item is in the itemlist.

    INPUT:
    item (dict) : derivative with "items","weight" and "moment"
    items(dict) : dictonary with the json file data

    OUTPUT:
    True / False result of whether or not item is in itemlist
    '''
    for i in range(len(itemlist)):
        if item["items"]==(itemlist[i])["items"] and item["weight"]==(itemlist[i])["weight"] and item["moment"]==(itemlist[i])["moment"]:
            return True
    return False

# def Clear(items,classes, derivative):
#     '''
#     This function checks if the input derivative include every one of the base items(no derivative)
#     and that each item apper only once

#     INPUT:
#     items(dict) : dictonary with the json file data
#     classes(dict): dictonary that contains the lists of item's indexs that belong to each group
#     derivative(dict): derivative with "items","weight" and "moment"

#     OUTPUT:
#     True / False result of whether or not the derivative include all base items *ONCE*
    
#     '''
#     base=[]
#     for i in classes["father"]:
#         if i not in classes["truth"]:
#             base.append(items["items"][i])
#     base
#     for j in base:
#         if j not in derivative["items"]:
#             return False
#     for derivative["items"].count(j)!=1:
#             return False
#     return True

def Delta_Weight(index,items):
    '''
    This function checks if the input item (based on is index) has delta weight .

    INPUT:
    index (int) : index of the item  
    items(dict) : dictonary with the json file data

    OUTPUT:
    True / False result of whether or not weight_delta is zero
    '''
    if items["weight_delta"][index]!=0:
        return True
    return False 


def Delta_CG(index,items):
    '''
    This function checks if the input item (based on is index) has delta cg .

    INPUT:
    index (int) : index of the item  
    items(dict) : dictonary with the json file data

    OUTPUT:
    True / False result of whether or not cg_d is zero
    '''
    if items["cg_d"][index]!=0:
        return True
    return False


def Children_Counter(items,item):
    '''
    This function counts the number of children for a specific item.

    INPUT:
    item (string) : item name
    items(dict) : dictonary with the json file data

    OUTPUT:
    The number of children for the specific item (int)
    '''
    counter=0
    for i in range(len(items["items"])):
        if items["father"][i]==item and items["father"][i]!=items["items"][i]:
            counter+=1
    return counter


def Classifier(items):
    '''
    This function classifies items into 1 (or more) of the folowing groups:
    priority - every item how isn't priority 1, childless - priorty 1 item without children,
    father - priorty 1 item with children, truth - priority 1 item with derivative and 
    delta - priority 1 item with delta weight or delta cg 

    INPUT:
    items(dict) : dictonary with the json file data

    OUTPUT:
    Dictonary that contains the lists of item's indexs that belong to each group
    '''
    classified={}
    priority=[]
    childless=[]
    father=[]
    truth=[]
    delta=[]
    for i in range(len(items["items"])):
        if items["father"][i]==items["items"][i]:
            if Children_Counter(items,items["items"][i])==0:
                childless.append(i)
                if items["derivative"][i]:
                    truth.append(i)
            else:
                father.append(i)
            if Delta_Weight(i,items) or Delta_CG(i,items) :
                delta.append(i)
        else:
            priority.append(i)
    classified={"priority":priority, "childless":childless, "father":father,"truth":truth, "delta":delta}
    return classified

def Delta_Derivative(derivative,i,items):
    '''
    This function grenerates derivatives for delta weight ans/or delta cg

    INPUT:
    items(dict) : dictonary with the json file data
    derivative(list) : list of derivatives(dict)
    i(int) : index of the item

    OUTPUT:
    Updates the Derviative list
    '''
    l=len(derivative)
    for j in range(l):
        if items["items"][i] in (derivative[j])["items"]:
            txt1=items["items"][i]+" weight"
            txt2=items["items"][i]+" cg"
            txt3=txt1+","+txt2
            if "deltas" in derivative[j]:
                txt1+=","+(derivative[j])["deltas"]
                txt2+=","+(derivative[j])["deltas"]
                txt3+=","+(derivative[j])["deltas"]
            dict1={
                "items":(derivative[j])["items"],
                "weight":(derivative[j])["weight"]+float(items["weight_delta"][i]),
                "moment" :(derivative[j])["moment"]+float(items["weight_delta"][i])*float(items["cg"][i]),
                "deltas":txt1
                }
            dict2={
                "items" : (derivative[j])["items"],
                "weight" : (derivative[j])["weight"],
                "moment" : (derivative[j])["moment"]+float(items["weight"][i])*float(items["cg_d"][i]),
                "deltas":txt2
                }
            m=float(items["weight_delta"][i])*float(items["cg"][i])+float(items["weight"][i])*float(items["cg_d"][i])+float(items["weight_delta"][i])*float(items["cg_d"][i])
            dict3={
                "items":(derivative[j])["items"],
                "weight":(derivative[j])["weight"]+float(items["weight_delta"][i]),
                "moment":(derivative[j])["moment"]+m,
                "deltas":txt3
                }
            if not Exist(dict1,derivative):
                derivative.append(dict1)    
            if not Exist(dict2,derivative):
                derivative.append(dict2)
            if not Exist(dict3,derivative):
                derivative.append(dict3)
    return

def True_Derivative(derivative,i,items):
    '''
    This function grenerates derivatives for items with "derivative"=True (specipicly Priority 1 items)

    INPUT:
    items(dict) : dictonary with the json file data
    derivative(list) : list of derivatives(dict)
    i(int) : index of the item

    OUTPUT:
    Updates the Derviative list
    '''
    l=len(derivative)
    m=(float(items["weight"][i])+float(items["weight_delta"][i]))*(float(items["cg"][i])+float(items["cg_d"][i]))
    for j in range(l):
        d = {
            "items":(derivative[j])["items"]+","+items["items"][i],
            "weight":(derivative[j])["weight"]+(float(items["weight"][i])+float(items["weight_delta"][i])),
            "moment" :(derivative[j])["moment"]+m
            }
        if not Exist(d,derivative):
            derivative.append(d) 
    return

def Derivative_Grenerator_P1(items,classified):
    '''
    This function grenerates derivatives for Priority 1 items

    INPUT:
    items(dict) : dictonary with the json file data
    classified(dict): dictonary that contains the lists of item's indexs that belong to each group

    OUTPUT:
    List of Derviatives(dict) of priority 1 items(childless items only)
    '''
    derivative=[]
    txt=""
    weight=0
    moment=0
    le=len(items["items"])
    # for i in classified["childless"]:
    #     if i not in classified["truth"]:
    #         txt+="  "+items["items"][i]
    #         weight+=float(items["weight"][i])
    #         moment+=(float(items["weight"][i])*float(items["cg"][i]))
    # derivative=[{"items":txt.strip(),"weight":weight,"moment":moment}]
    for i in range(le):
        if i not in classified["priority"]:
            if i not in classified["truth"]:
                txt+=','+items["items"][i]
                txt=txt.strip(',')
                weight+=float(items["weight"][i])
                moment+=(float(items["weight"][i])*float(items["cg"][i]))
    derivative=[{"items":txt.strip(),"weight":weight,"moment":moment}]
    for i in classified["childless"]:
        if i in classified["truth"]:
            True_Derivative(derivative,i,items)
    for i in range(len(items)):
        if i not in classified["priority"]:
            if i in classified["delta"]:
                Delta_Derivative(derivative,i,items)
    return derivative

# A function to grenerate a list of physical derivative based on order of loading 
# def Child_Derivative(mode,modelist,items,classified,ind):
#     '''
#     This function grenerates a list of physical derivatives based on order of loading (not working)

#     INPUT:
#     items(dict) : dictonary with the json file data
#     classified(dict): dictonary that contains the lists of item's indexs that belong to each group
#     modelist(list): list of derivatives(dict)
#     mode(dict): dictonary that contains information about a specific father

#     OUTPUT:
#     Updates the modelist
#     '''
#     item=mode["items"]
#     lastitem=item.rsplit("  ")[-1]
#     # if not Exist(mode,modelist):
#     if ind==0:
#         modelist.append(mode)
#     else:
#         Appender(modelist,mode)  
    # devitems=[]
#     if Children_Counter(items,lastitem)>0:
#         devitems=Items(mode,items,classified)
#         for j in range(len(devitems)):
#             Child_Derivative(devitems[j],modelist,items,classified,ind)
        
#     return
# def Appender(modelist,mode):
#     le=len(modelist)
#     for i in range(le):
#         string=str(modelist[i]["items"])+"  "+str(mode["items"])
#         weight=float(modelist[i]["weight"])+(float(mode["weight"]))
#         moment=float(modelist[i]["moment"])+(float(mode["moment"]))
#         d = {
#             "items" : string,
#             "weight" : weight,
#             "moment" : moment
#         }
#         modelist.append(d)
#     return
#  A function to grenerate a list of physical derivative based on order of loading
def Child_Derivative2(listitem,items,classified):
    '''
    This function grenerates a list of physical derivatives based on order of loading (fixed) 

    INPUT:
    items(dict) : dictonary with the json file data
    classified(dict): dictonary that contains the lists of item's indexs that belong to each group
    listitem(list): list of derivatives(dict)

    OUTPUT:
    Updates the listitem
    '''
    fathers=[]
    devitems=[]
    for i in range(len(items["items"])):
        if Children_Counter(items,items["items"][i])!=0:
            fathers.append(i)
    for j in fathers:
        item=items["items"][j]
        devitems=Items(item,listitem,items,classified)
        for i in range(len(devitems)):
            listitem.append(devitems[i])
    return 
        
# A function to generates Father-Son derivatives
def Items(item,itemlist,items,classified):
    '''
    This function grenerates derivatives based on Father-Son relations

    INPUT:
    items(dict) : dictonary with the json file data
    listitem(list): list of derivatives(dict)
    classified(dict): dictonary that contains the lists of item's indexs that belong to each group
    item (dict) : dictonary of a item/s with "items","weight" and "moment"

    OUTPUT:
    List of Derviatives(dict) grenerated based on  Father-Son relations
    '''
    dev=[]
    for j in range(len(itemlist)):
        split=itemlist[j]["items"].split(item)
        string=split[0]+item
        weight=0
        moment=0
        for i in classified["priority"]:
            if items["father"][i]==item:
                string+=','+str(items["items"][i])+split[-1]
                string=string.strip(',')
                weight=float(itemlist[j]["weight"])+(float(items["weight"][i])+float(items["weight_delta"][i]))
                m=(float(items["weight"][i])+float(items["weight_delta"][i]))*(float(items["cg"][i])+float(items["cg_d"][i]))
                moment=float(itemlist[j]["moment"])+m
                d = {
                    "items" : string,
                    "weight" : weight,
                    "moment" : moment
                    }
                if not Exist(d,dev):
                    dev.append(d) 
    return dev
# creating all physical derivatives            
def Physical_Derivative(items):
    '''
    This function grenerates all physical derivatives of a given set of items

    INPUT:
    items(dict) : dictonary with the json file data

    OUTPUT:
    List of all physical Derviatives(dict) 
    '''
    # derlist=[]
    # itemlist=[]
    Derivatives=[]
    # classifing the items items
    classes=Classifier(items)
    Derivatives=Derivative_Grenerator_P1(items, classes)
    Child_Derivative2(Derivatives,items, classes)
    # for i in classes["father"]:
    #     m=float(items["weight"][i])*float(items["cg"][i])
    #     derlist=[{"items":items["items"][i],"weight":items["weight"][i],"moment":m}]
    #     if i in classes["delta"]:
    #         Delta_Derivative(derlist,i,items)
    #     for j in range(len(derlist)):
    #         Child_Derivative(derlist[j],itemlist,items,classes,j)
    
    # (need to fix CLEAR)
    
    # i=0
    # while i in range(len(Derivatives)):        
    #     if Clear(base,Derivatives[i])==False:
    #         Derivatives.pop(i)
    #     else:
    #         i+=1
            

    # length=len(Derivatives)
    # for i in range(length):
    #     for j in range(len(itemlist)):
    #         dict1={
    #             "items":(Derivatives[i])["items"]+"  "+(itemlist[j])["items"],
    #             "weight":float((Derivatives[i])["weight"])+float((itemlist[j])["weight"]),
    #             "moment":float((Derivatives[i])["moment"])+float((itemlist[j])["moment"])
    #             }
    #         Derivatives.append(dict1)
    return Derivatives
# Creating a list with all physical derivatives for each tail number
def Derivative_Grenerator(items):
    '''
    This function grenerates all physical derivatives for each tail number of a given set of items 
    and tail numbers

    INPUT:
    items(dict) : dictonary with the json file data

    OUTPUT:
    List of all physical Derviatives(dict) with tail_number, items, total weight and total cg
    '''
    DerPerPlane=[]
    DerivativeList=[]
# creating a dictonty for the planes
    plane={"Tail_num":(items["aircrafts"][0])["Tail_num"],"Weight":(items["aircrafts"][1])["Weight"],"CG":(items["aircrafts"][2])["CG"]}
    Derivatives=Physical_Derivative(items)
    for i in range(len(plane["Tail_num"])):
        DerPerPlane.clear()
        for j in range(len(Derivatives)):
            # moment=(float(plane["Weight"][i])*float(plane["CG"][i])+float((Derivatives[j])["moment"]))
            cg=(float(plane["Weight"][i])*float(plane["CG"][i])+float((Derivatives[j])["moment"]))/(float((Derivatives[j])["weight"])+float(plane["Weight"][i]))
            if "deltas" in Derivatives[j]:
                dict2={
                    "items":(Derivatives[j])["items"],
                    "Weight":float((Derivatives[j])["weight"])+float(plane["Weight"][i]),
                    "CG":cg,
                    # "Moment":moment,
                    "deltas":(Derivatives[j])["deltas"]
                    }
            else:
                dict2={
                    "items":(Derivatives[j])["items"],
                    "Weight":float((Derivatives[j])["weight"])+float(plane["Weight"][i]),
                    "CG":cg
                    # "Moment":moment
                    }
            DerPerPlane.append(dict2)
        DerivativeList.append({"Tail Number":plane["Tail_num"][i],"Derivatives":DerPerPlane})
    return DerivativeList

# Main
datajson=open("C:/Users/Gilad Timar/Documents/עבודה/scripts/dummyClientRequest0.json", 'r')
items=json.load(datajson)
DerivativeList=Derivative_Grenerator(items)
print(DerivativeList)    
