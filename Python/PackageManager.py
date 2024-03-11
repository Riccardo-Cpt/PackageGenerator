import subprocess
import sys
import logging
import os

def creaListaTabelle(lista1, lista2=list(), lista3=list()):
    listatabelle=lista1+lista2+lista3
    return listatabelle

def createAreaList(listatabelle): 
    listaaree=[]
    for tabella in listatabelle: 
        if tabella[0:3] not in listaaree:
            listaaree.append(tabella[0:3])
    return listaaree
            
def createSubAreaList(listatabelle): 
    listasubaree=[]
    for tabella in listatabelle: 
        if tabella[0:4] not in listasubaree:
            listasubaree.append(tabella[0:4])
    return listasubaree

if __name__ == "__main__":
    try:
        
        ###################
        #Liste di tabelle input
        list1=sys.argv[1]
        list2=sys.argv[2]
        list3=sys.argv[3]
        
        #Flag per indicare se deve essere creato il file manager o meno
        flag_manager=sys.argv[4]
        
        #Ambiente di rilascio(TEST o PROD)
        ambiente=sys.argv[5]
        
        #Percorsi file log e script richiamati
        log_path=sys.argv[6]
        script_path=sys.argv[7]
        out_path=sys.argv[8]
        ###################
        
        #Generazione di un file di log globale
        Log=os.path.join(log_path,os.path.basename(__file__)[:-3])+'.log'
        logging.basicConfig(filename=Log,format='%(message)s', filemode='w')
        logger=logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        logger.info('#########################################')
        logger.info('Script {} in esecuzione...'.format(os.path.basename(__file__)))
        logger.info('#########################################\n')
        
        #trasformazioni variabili stringa in input in liste
        list1=[x.strip() for x in list1.split(',') if x.strip()]
        list2=[x.strip() for x in list2.split(',') if x.strip()]
        list3=[x.strip() for x in list3.split(',') if x.strip()]
        
        #Richiamo funzione concatenazione liste tabelle
        tabelle=creaListaTabelle(list1, list2, list3)
        
        #Richiamo funzione estrazione aree
        aree=createAreaList(tabelle)
        
        #Richiamo funzione estrazione subaree
        subaree=createSubAreaList(tabelle)
        logger.info('Input ricevuti: ')
        logger.info('Tabelle: {}'.format(tabelle))
        logger.info('Aree: {}'.format(aree))
        logger.info('Subaree: {}'.format(subaree))
        logger.info('\n')
        
        #Conversione liste generate a stringhe per poterle passare ai sottoprocessi
        aree=','.join(aree)
        subaree=','.join(subaree)
        tabelle=','.join(tabelle)
        
        #Richiamo script WriteManifest.py per creazione package manifest sotto la folder che prende il nome da RFC inserito
        logger.info('--> Richiamo script WriteManifest.py...\nVariabili passate:\n -Aree: {}\n -Subaree: {}\n -Tabelle: {}\n -File Manager: {}\n -PathLog: {}\n -PathOutput: {}'.format(aree,subaree,tabelle,flag_manager,log_path,out_path))
        write_manifest_path=os.path.join(script_path,'WriteManifest.py') #'/GFS/infa/infa_shared/DGOV/Script/UTILITY/WriteManifest.py'
        subprocess.call([sys.executable,write_manifest_path,aree,subaree,tabelle,flag_manager,log_path,out_path])
        
        #Richiamo script WritePmrep_import.py per creazione del pmrep_import sotto il subfolder generico
        logger.info('\n')
        out_path=os.path.join(out_path,'generico')
        logger.info('--> Richiamo script WritePmrep_import.py...\nVariabili passate:\n -Aree: {}\n -Subaree: {}\n -File Manager: {}\n -ambiente: {}\n -PathLog: {}\n -PathOutput: {}'.format(aree,subaree,flag_manager,ambiente,log_path,out_path))
        write_pmrep_path=os.path.join(script_path,'WritePmrep_import.py')
        subprocess.call([sys.executable,write_pmrep_path,aree,subaree,flag_manager,ambiente,log_path,out_path])
        
        with open(os.path.join(log_path,'temp_areas.txt'), 'w') as temp_file:
            temp_file.write(aree)
        
        sys.exit(0)
    
    except Exception as e:
        logging.basicConfig(filename=Log,format='%(asctime)s %(message)s', filemode='w')
        logger=logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.error('Si è verificato il seguente errore:\n%s' %e)
        sys.exit(1)
