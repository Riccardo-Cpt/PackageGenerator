#Script per la creazione del file di pmrep_import. Attualmente non è in grado di gestire un rilascio in ambiente PROD

import sys
import os
import logging

def WF_IL(subarea, ambiente='TEST'):
    
    if ambiente=='TEST':
        wf_il= "pmrep connect -r REPDQ_" +ambiente+" -d ETLDWH9_"+ambiente+" -n Administrator -X INFA_PW -s Native"+chr(10)+"./update_return_codes.sh $?"+chr(10)+"pmrep objectimport -i /GFS/infa/infa_shared/nolio/WF_IL_000_"+subarea+"_001.xml -c /GFS/infa/infa_shared/nolio/DTD_WF_IL_000_"+subarea+"_001.dtd -l /GFS/infa/infa_shared/nolio/DTD_WF_IL_000_"+subarea+"_001.log"+chr(10)+"./update_return_codes.sh $?"+2*chr(10)
    
    elif ambiente=='PROD':
        wf_il= "pmrep connect -r REPDQ_" +ambiente+" -d ETLDWH9_"+ambiente+" -n opcetl -X INFA_PW -s ETL_OPC"+chr(10)+"./update_return_codes.sh $?"+chr(10)+"pmrep objectimport -i /GFS/infa/infa_shared/nolio/WF_IL_000_"+subarea+"_001.xml -c /GFS/infa/infa_shared/nolio/DTD_WF_IL_000_"+subarea+"_001.dtd -l /GFS/infa/infa_shared/nolio/DTD_WF_IL_000_"+subarea+"_001.log"+chr(10)+"./update_return_codes.sh $?"+2*chr(10)

    else:
        logger.error('Error: Ambiente specificato scorretto: {}'.format(ambiente))
        exit(1)
        
    return wf_il


def WF_Tecnico(area, element, ambiente='TEST'):

    if ambiente=='TEST':
        wf_tech= "pmrep connect -r REPDQ_"+ambiente+" -d ETLDWH9_"+ambiente+" -n Administrator -X INFA_PW -s Native"+chr(10)+"./update_return_codes.sh $?"+chr(10)+"pmrep objectimport -i /GFS/infa/infa_shared/nolio/WF_IL_000_"+area+element+".xml -c /GFS/infa/infa_shared/nolio/DTD_WF_IL_000_"+area+element+".dtd -l /GFS/infa/infa_shared/nolio/DTD_WF_IL_000_"+area+element+".log"+chr(10)+"./update_return_codes.sh $?"+2*chr(10)
    
    elif ambiente=='PROD':
        wf_tech= "pmrep connect -r REPDQ_"+ambiente+" -d ETLDWH9_"+ambiente+" -n opcetl -X INFA_PW -s ETL_OPC"+chr(10)+"./update_return_codes.sh $?"+chr(10)+"pmrep objectimport -i /GFS/infa/infa_shared/nolio/WF_IL_000_"+area+element+".xml -c /GFS/infa/infa_shared/nolio/DTD_WF_IL_000_"+area+element+".dtd -l /GFS/infa/infa_shared/nolio/DTD_WF_IL_000_"+area+element+".log"+chr(10)+"./update_return_codes.sh $?"+2*chr(10)
    
    else:
        logger.error('Error: Ambiente specificato scorretto: {}'.format(ambiente))
        exit(1)

    return wf_tech
    

if __name__ == "__main__":

    try:

        ####################
        aree=sys.argv[1]
        subaree=sys.argv[2]
        flag_manager=sys.argv[3]
        ambiente=sys.argv[4]
        
        #Percorsi file log e script richiamati
        log_path=sys.argv[5]
        OutFile_path=sys.argv[6]
        ####################
        
        #Inizializzazione ambienti di scrittura
        aree_out= aree.replace(",","_")
        file_name='pmrep_import'
        Output= os.path.join(OutFile_path, file_name)
        Log=os.path.join(log_path,os.path.basename(__file__)[:-3])+'.log'
        
        logging.basicConfig(filename=Log,format='%(asctime)s %(message)s', filemode='w')
        logger=logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        logger.info('==> Script {} in esecuzione...'.format(os.path.basename(__file__)))
        
        aree=aree.split(',')
        subaree=subaree.split(',')
        
        logger.info('Lista aree {}'.format(aree))
        logger.info('Lista subaree {}'.format(subaree))
        
        #Configurazione ambiente, da aggiungere calcolo connessioni variabile a seconda se il rilascio avvenga in test o prod.
        
        logger.info('-->Inizo creazione file per ambiente {}'.format(ambiente))
        
        with open(Output, 'w') as pmrep_import:
        
            for subarea in subaree:
            
                logger.info('Inizializzo subarea {}'.format(subarea))
                wf_il = WF_IL(subarea=subarea, ambiente=ambiente)
                
                pmrep_import.write(wf_il)
            
            for area in aree:
            
                logger.info('Inizializzo area {}'.format(area))
                wf_sem12=WF_Tecnico(area, element='_SEMAPHORE_1_2', ambiente=ambiente)
                wf_sem22=WF_Tecnico(area, element='_SEMAPHORE_2_2', ambiente=ambiente)
                wf_perm_file=WF_Tecnico(area, element='_TEST_PERMISSION_FILE', ambiente=ambiente)
                wf_ss_file=WF_Tecnico(area, element='_TEST_SOURCE_SYSTEM_FILE', ambiente=ambiente)
                
                pmrep_import.write(wf_sem12+wf_sem22+wf_perm_file+wf_ss_file)
                
            #verifica se deve essere aggiunto WF_IL_000_FILE_MANAGER
            if flag_manager=='S':
                wf_file_manager=WF_Tecnico(area='', element='FILE_MANAGER', ambiente=ambiente)
                
                pmrep_import.write(wf_file_manager)
                
                
        logger.info('==> Scrittura pmrep_import terminata con successo nel folder {}'.format(OutFile_path))
                
        sys.exit(0)
    
    except Exception as e:
        logging.basicConfig(filename=Log,format='%(asctime)s %(message)s', filemode='w')
        logger=logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.error('Si è verificato il seguente errore:\n%s' %e)
        sys.exit(1)