#Script per la generazione del file di PackageManifest.xml. Riceve in input le liste di tutte le aree, subaree e tabelle coinvolte nel rilascio e ne crea il file di conseguenza

import os
import sys
import json
import time
import logging


#Funzione generazione prime righe iniziali costanti
def createHeader():
    header = "<PackageManifest>"+chr(10)+4*chr(32)+"<Description value="+chr(34)+chr(34)+chr(47)+">"+chr(10)+4*chr(32)+"<version value="+chr(34)+chr(34)+chr(47)+">"+chr(10)+4*chr(32)+"<Amministrazione value="+chr(34)+'yes'+chr(34)+chr(47)+">"+chr(10)+4*chr(32)+"<StartTemporizzato value="+chr(34)+'yes'+chr(34)+chr(47)+">"+chr(10)+4*chr(32)+"<Artifacts>"+chr(10)

    return header

#Funzione generazione sezioni xml e dtd
def createXmlDTDBase(area, element):
    xml=2*chr(9)+"<Artifact>"+chr(10)+12*chr(32)+"<alias value="+chr(34)+"WF_IL_000_"+area+element+".xml"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<filename value="+chr(34)+"WF_IL_000_"+area+element+".xml"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<version value="+chr(34)+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<type value="+chr(34)+"generico"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute DirectoryDestination="+chr(34)+"/GFS/infa/infa_shared/nolio"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute owner="+chr(34)+"infa"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute umask="+chr(34)+"664"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute unzip="+chr(34)+"null"+chr(34)+chr(47)+">"+chr(10)+8*chr(32)+"<"+chr(47)+"Artifact>"+chr(10)
    dtd=2*chr(9)+"<Artifact>"+chr(10)+12*chr(32)+"<alias value="+chr(34)+"DTD_WF_IL_000_"+area+element+".dtd"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<filename value="+chr(34)+"DTD_WF_IL_000_"+area+element+".dtd"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<version value="+chr(34)+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<type value="+chr(34)+"generico"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute DirectoryDestination="+chr(34)+"/GFS/infa/infa_shared/nolio"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute owner="+chr(34)+"infa"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute umask="+chr(34)+"664"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute unzip="+chr(34)+"null"+chr(34)+chr(47)+">"+chr(10)+8*chr(32)+"<"+chr(47)+"Artifact>"+chr(10)

    return xml+dtd

#Funzione generazione sezioni file dei parametri
def createParamBase(area,subarea,sorg='A'):
    param1=2*chr(9)+"<Artifact>"+chr(10)+12*chr(32)+"<alias value="+chr(34)+"param_file_"+subarea+".txt"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<filename value="+chr(34)+"param_file_"+subarea+".txt"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<version value="+chr(34)+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<type value="+chr(34)+"generico"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute DirectoryDestination="+chr(34)+"/GFS/infa/infa_shared/DGOV/BWParam/"+area+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute owner="+chr(34)+"infa"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute umask="+chr(34)+"775"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute unzip="+chr(34)+"null"+chr(34)+chr(47)+">"+chr(10)+8*chr(32)+"<"+chr(47)+"Artifact>"+chr(10)
    param2=2*chr(9)+"<Artifact>"+chr(10)+12*chr(32)+"<alias value="+chr(34)+"param_file_"+subarea+"_"+subarea+sorg+".txt"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<filename value="+chr(34)+"param_file_"+subarea+"_"+subarea+sorg+".txt"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<version value="+chr(34)+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<type value="+chr(34)+"generico"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute DirectoryDestination="+chr(34)+"/GFS/infa/infa_shared/DGOV/BWParam/"+area+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute owner="+chr(34)+"infa"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute umask="+chr(34)+"775"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute unzip="+chr(34)+"null"+chr(34)+chr(47)+">"+chr(10)+8*chr(32)+"<"+chr(47)+"Artifact>"+chr(10)
    
    return param1+param2

#Funzioni generazione sezioni shell
def createCONNBase(area,subarea,element,sorg='A'):
    shellCONN=2*chr(9)+"<Artifact>"+chr(10)+12*chr(32)+"<alias value="+chr(34)+element+subarea+"_"+subarea+sorg+".sh"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<filename value="+chr(34)+element+subarea+"_"+subarea+sorg+".sh"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<version value="+chr(34)+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<type value="+chr(34)+"generico"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute DirectoryDestination="+chr(34)+"/GFS/infa/infa_shared/DGOV/Script/"+area+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute owner="+chr(34)+"infa"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute umask="+chr(34)+"774"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute unzip="+chr(34)+"null"+chr(34)+chr(47)+">"+chr(10)+8*chr(32)+"<"+chr(47)+"Artifact>"+chr(10)
    
    return shellCONN
    
def createSEMase(area,subarea,element):
    shellSEM=2*chr(9)+"<Artifact>"+chr(10)+12*chr(32)+"<alias value="+chr(34)+element+subarea+".sh"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<filename value="+chr(34)+element+subarea+".sh"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<version value="+chr(34)+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<type value="+chr(34)+"generico"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute DirectoryDestination="+chr(34)+"/GFS/infa/infa_shared/DGOV/Script/"+area+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute owner="+chr(34)+"infa"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute umask="+chr(34)+"774"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute unzip="+chr(34)+"null"+chr(34)+chr(47)+">"+chr(10)+8*chr(32)+"<"+chr(47)+"Artifact>"+chr(10)
    
    return shellSEM

def createPERMBase(area,subarea,element,tabella,sorg='A'):
    shellPERM=2*chr(9)+"<Artifact>"+chr(10)+12*chr(32)+"<alias value="+chr(34)+element+subarea+"_"+subarea+sorg+"_"+tabella+".sh"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<filename value="+chr(34)+element+subarea+"_"+subarea+sorg+"_"+tabella+".sh"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<version value="+chr(34)+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<type value="+chr(34)+"generico"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute DirectoryDestination="+chr(34)+"/GFS/infa/infa_shared/DGOV/Script/"+area+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute owner="+chr(34)+"infa"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute umask="+chr(34)+"774"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute unzip="+chr(34)+"null"+chr(34)+chr(47)+">"+chr(10)+8*chr(32)+"<"+chr(47)+"Artifact>"+chr(10)
    
    return shellPERM

def permanenti(element='',fileType='',Outdir=''):
    perm=2*chr(9)+"<Artifact>"+chr(10)+12*chr(32)+"<alias value="+chr(34)+element+fileType+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<filename value="+chr(34)+element+fileType+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<version value="+chr(34)+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<type value="+chr(34)+"generico"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute DirectoryDestination="+chr(34)+Outdir+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute owner="+chr(34)+"infa"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute umask="+chr(34)+"774"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute unzip="+chr(34)+"null"+chr(34)+chr(47)+">"+chr(10)+8*chr(32)+"<"+chr(47)+"Artifact>"+chr(10)
    
    return perm

def permanentiRoot(element='',fileType='',Attribute='SCRIPT',Attorder='1'):
    perm=2*chr(9)+"<Artifact>"+chr(10)+12*chr(32)+"<alias value="+chr(34)+element+fileType+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<filename value="+chr(34)+element+fileType+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<version value="+chr(34)+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<type value="+chr(34)+"post script"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute type="+chr(34)+Attribute+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute owner="+chr(34)+"infa"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute umask="+chr(34)+"774"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute order="+chr(34)+Attorder+chr(34)+chr(47)+">"+chr(10)+8*chr(32)+"<"+chr(47)+"Artifact>"+chr(10)
    
    return perm

#Funzione generazione righe di chiusura manifest
def righeChiusura():
    righe=4*chr(32)+"<"+chr(47)+"Artifacts>"+chr(10)+"<"+chr(47)+"PackageManifest>"
    
    return righe
    
def FileManager():
    xml=2*chr(9)+"<Artifact>"+chr(10)+12*chr(32)+"<alias value="+chr(34)+"WF_IL_000_FILE_MANAGER.xml"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<filename value="+chr(34)+"WF_IL_000_FILE_MANAGER.xml"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<version value="+chr(34)+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<type value="+chr(34)+"generico"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute DirectoryDestination="+chr(34)+"/GFS/infa/infa_shared/nolio"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute owner="+chr(34)+"infa"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute umask="+chr(34)+"664"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute unzip="+chr(34)+"null"+chr(34)+chr(47)+">"+chr(10)+8*chr(32)+"<"+chr(47)+"Artifact>"+chr(10)
    dtd=2*chr(9)+"<Artifact>"+chr(10)+12*chr(32)+"<alias value="+chr(34)+"DTD_WF_IL_000_FILE_MANAGER.dtd"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<filename value="+chr(34)+"DTD_WF_IL_000_FILE_MANAGER.dtd"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<version value="+chr(34)+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<type value="+chr(34)+"generico"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute DirectoryDestination="+chr(34)+"/GFS/infa/infa_shared/nolio"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute owner="+chr(34)+"infa"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute umask="+chr(34)+"664"+chr(34)+chr(47)+">"+chr(10)+12*chr(32)+"<attribute unzip="+chr(34)+"null"+chr(34)+chr(47)+">"+chr(10)+8*chr(32)+"<"+chr(47)+"Artifact>"+chr(10)

    return xml+dtd

if __name__ == "__main__":
#il main restituisce codici 0 o 1 a seconda ci siano stati errori o meno, nel file log viene registrato leventuale codice di errore
    try:
        t=time.time()

        ################DICHIARAZIONE INPUT###################
        #Stringhe input
        aree=sys.argv[1]#aree=['PRB','AMG']
        subaree=sys.argv[2]
        tabelle=sys.argv[3]
        flag_manager=sys.argv[4]
        
        #Percorsi file log e script richiamati
        log_path=sys.argv[5]
        OutFile_path=sys.argv[6]
        
        ######################################################
        
        #Inizializzazione ambienti di scrittura
        aree_out= aree.replace(",","_")
        file_name='PackageManifest.xml'
        Output= os.path.join(OutFile_path, file_name)
        Log=os.path.join(log_path,os.path.basename(__file__))+'.log'
        
        logging.basicConfig(filename=Log,format='%(asctime)s %(message)s', filemode='w')
        logger=logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        
        logger.info('==> Script WriteManifest in esecuzione...')
        
        #Conversione stringhe in input a oggetti lista python
        aree=aree.split(',')
        subaree=subaree.split(',')
        tabelle=tabelle.split(',')
        logger.info('Lista aree {}'.format(aree))
        logger.info('Lista subaree {}'.format(subaree))
        logger.info('Lista tabelle {}'.format(tabelle))

        with open(Output, 'w') as manifest:
        
            # Scrittura righe di header e file di UpdateReturnCodes, pmrep_import, pmrep_import_root
            header=createHeader()
            updateRetCodes=permanenti(element='update_return_codes',fileType='.sh'
                                        ,Outdir='/GFS/infa/infa_shared/nolio')
            
            pmrep_import=permanenti(element='pmrep_import',fileType=''
                                        ,Outdir='/GFS/infa/infa_shared/nolio')

            pmrep_import_root=permanentiRoot(element='pmrep_import_root',fileType='.sh',Attribute='SCRIPT')
            manifest.write(header+updateRetCodes+pmrep_import+pmrep_import_root)
            
            #In relazione al flag passato, creerà un oggetto .xml ed uno .dtd se flag_manager = S, altrimenti skippa questo step
            if flag_manager=='S':
                manifest.write(FileManager())
            
            #Tre loop annidiati, primo cicla su aree, secondo cicla su sottoaree appartenenti l'area corrente, il terzo su tutte le tabelle appartenenti alla sottoarea corrente
            for area in aree:
            
                logger.info('Inizializzo area {}'.format(area))
                
                #Scrittura dei WF_IL per area passata dal parametro
                Sem1 = createXmlDTDBase(area=area, element="_SEMAPHORE_1_2")
                Sem2 = createXmlDTDBase(area=area, element="_SEMAPHORE_2_2")
                
                PermFile = createXmlDTDBase(area=area, element="_TEST_PERMISSION_FILE")
                TestSSFile = createXmlDTDBase(area=area, element="_TEST_SOURCE_SYSTEM_FILE")
                manifest.write(Sem1+Sem2+PermFile+TestSSFile)
                
                for subarea in [sub for sub in subaree if area in sub]:
                    
                    logger.info('Inizializzo subarea {}'.format(subarea))
                    
                    #Scrittura dei WF_IL per subarea passata dal parametro
                    WF_IL= createXmlDTDBase(subarea, element="_001")
                    manifest.write(WF_IL)
                    
                    #Scrittura dei file dei parametri, sorgente default = A, attualmente non sono gestiti rilasci con più sorgenti
                    Param=createParamBase(area,subarea)
                    manifest.write(Param)
                    
                    #Scrittura shell  per subarea passata dal parametro
                    TestConn=createCONNBase(element="TEST_CONNECTION_",area=area,subarea=subarea,sorg='A')
                    TestConnFile=createCONNBase(element="TEST_CONNECTION_FILE_",area=area,subarea=subarea,sorg='A')
                    
                    Sem1=createSEMase(element="TEST_SEMAPHORE_1_2_",area=area,subarea=subarea)
                    Sem2=createSEMase(element="TEST_SEMAPHORE_2_2_",area=area,subarea=subarea)
                    
                    manifest.write(TestConn+TestConnFile)
                    manifest.write(Sem1+Sem2)
                    
                    for tabella in [tab for tab in tabelle if subarea in tab]:
                        #Scrittura shell TEST_PERMISSION e TEST_PERMISSION_FILE per ciascuna tabella input
                        TestPerm=createPERMBase(element="TEST_PERMISSION_",area=area,subarea=subarea,tabella=tabella,sorg='A')
                        TestPermFile=createPERMBase(element="TEST_PERMISSION_FILE_",area=area,subarea=subarea,tabella=tabella,sorg='A')
                        
                        manifest.write(TestPerm+TestPermFile)
                        
                    logger.info('Termintata scrittura per subarea {}'.format(subarea))
            
                logger.info('Termintata scrittura per area {}'.format(area))
            
            chiusura=righeChiusura()
            manifest.write(chiusura)
            
        logger.info('==> Scrittura manifest terminata con successo, tempo di run totale: {}'.format(str(time.time()-t)))


        sys.exit(0)
    
    except Exception as e:
        logging.basicConfig(filename=Log,format='%(asctime)s %(message)s', filemode='w')
        logger=logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.error('Si è verificato il seguente errore:\n%s' %e)
        sys.exit(1)
