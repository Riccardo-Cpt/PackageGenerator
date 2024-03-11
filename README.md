# PackageGenerator
Automatization of Release Package creation for a private client

This software is meant to be runned with Informatica Powercenter 

Param file: to run the software is necessary to write a list of all the tables meant to be realeased. All the tables must follow a strict naming convention.
Three variables are assigned to store lists of table names ($$V_WF_LISTA1, $$V_WF_LISTA2, $$V_WF_LISTA3), max 2000 char each

Other optional parameters are displayed in the following table:

![image](https://github.com/Riccardo-Cpt/PackageGenerator/assets/61077368/a36dbc90-6721-4bc4-88fd-be68409aea7e)

The workflow follows the following architecture:

![image](https://github.com/Riccardo-Cpt/PackageGenerator/assets/61077368/ebcb0c3a-ab05-4b09-84b0-2dd02665741c)

In this table is shortly described each process:
![image](https://github.com/Riccardo-Cpt/PackageGenerator/assets/61077368/197f47e9-819c-43bc-a0e8-b822f27fd919)


Technical details:

5.1	Cmd_Create_LogDir
A simple command to crate a log directory, specific for the release environment and the realease code

5.2	CreateBackbone.sh
Una shell col compito di generare il folder relativo il pacchetto di rilascio e tutte le sottocartelle associate. Inoltre genererà le shell di pmrep_import_root.sh e update_return_codes.sh. La naming del pacchetto segue lo standard BPER:

Rilascio_<ambiente rilascio>_RFC_<codice RFC>_<data rilascio>

Inoltre, partendo dal folder principale, i subfolder generati rispetteranno le alberature:

•	./<RFC>/generico
•	./<RFC>/post script
•	./<RFC>/post script DB
•	./<RFC>/pre script
•	./<RFC>/pre script DB
•	./ORACLE/DEPLOY
•	./ORACLE/SCRIPT
 
5.3	PackageManager.py
Ha lo scopo di ricevere le tabelle RDL oggetto del rilascio, e dalla loro naming ricavarne:
-	Le aree coinvolte 
-	Le sottoaree coinvolte 
-	Richiamare lo script WriteManifest.py
-	Richiamare lo script WritePmrep_import.py
 
5.3.1	WriteManifest.py
Ha come scopo la generazione del PackageManifest.xml, un catalogo di tutti gli oggetti contenuti all’ interno del pacchetto da installare nel momento del rilascio.

Inizia con la scrittura delle componenti fisse:
-	La parte iniziale del file
-	Update_return_codes.sh
-	pmrep_import
-	pmrep_import_root.sh
-	In caso di flag positivo, l’oggetto relativo al file manager (.xml e .dtd)

Dopodichè inizia ad iterare per area corrente, generando i workflow relativi:
-	Gli oggetti relativi ai workflow di semaforo, sia 1_2 che 2_2 (.xml e .dtd)
-	Gli oggetti relativi al workflow TEST_PERMISSION (.xml e .dtd)
-	Gli oggetti relativi al workflow TEST_SOURCE_SYSTEM_FILE (.xml e .dtd)

Poi, inizierà ad iterare per sottoarea, generando:
-	Gli oggetti relativi al WF RDL (.xml e .dtd)
-	I file dei parametri per il workflow RDL (.txt)
-	La shell TEST_CONNECTION (.sh)
-	La shell TEST_CONNECTION_FILE (.sh)
-	La shell TEST_SEMAPHORE_1_2_ (.sh)
-	La shell TEST_SEMAPHORE_2_2_ (.sh)

Infine, itererà per ciascuna tabella appartenente alla sottoarea in esame, generando:
-	La shell TEST_PERMISSION (.sh)
-	La shell TEST_PERMISSION_FILE (.sh)

Terminate tutte le iterazioni scriverà su file:
-	Righe di chiusura del file


5.3.2	WritePmrep_import.py
Ha come scopo la generazione del file pmrep_import, contenente tutti i comandi di import dei Worfklow presenti nel pacchetto di rilascio. Lo script si limita ad iterare per tutte le sottoaree e generare di conseguenza tutti i comandi di import per ciascun Workflow associato. Al termine di questa operazione, se necessario genera un comando per l’import del WF_IL_000_FILE_MANAGER
 
5.4	FillPackage.sh
Script col compito di leggere il file PackageManifest.xml, e per ogni elemento contenuto ricercarne la posizione e copiarlo all’interno del pacchetto, sotto il subfolder /generico, nel dettaglio:

-	Shell: effettua un comando di copy per copiare la shell citata nel Manifest e situata nel folder GFS\infa\infa_shared\DGOV\Script\<area>\ all’interno del folder di rilascio
-	ParamFile: effettua un comando di copy per copiare la shell citata nel Manifest e situata nel folder GFS\infa\infa_shared\DGOV\BWParam\<area>\ all’interno del folder di rilascio
-	Workflow: effettua un export direttamente dal repository di informatica, ricercando per folder associato e nome censito nel Manifest
-	File DTD: questi file vengono generati direttamente all’interno della shell.

Terminato il riempimento del subfolder /generico, i seguenti puntamenti presenti nei vari file verranno modificati, a seconda dell’ambiente di rilascio

Nel caso di un rilascio in TEST:
-	ISDQ_DEV  ISDQ_TEST
-	ETLDWH9_SVIL  ETLDWH9_TEST

Nel caso di un rilascio in PROD:
-	ISDQ_TEST  ISDQ_PROD
-	ETLDWH9_TEST  ETLDWH9_PROD
-	DW_ORACLE_EDW_DWETL_STND  DW_ETL_X_ORA_EDWP_DWETL_STND

 
5.5	GenerateDeploy.sh
Shell col compito di leggere gli script Oracle depositati nel folder dedicato, spostarli nel pacchetto di rilascio e generare il file di Deploy.sql:

Folder dedicato: \\infadwhs.gbbper.priv\infa_shared\DGOV\Script\UTILITY\PackageGenerator\ORACLE\<RFC>
Folder Ouptut script: \\infadwhs.gbbper.priv\infa_shared\DGOV\Script\UTILITY\PackageGenerator\<Nome  Pacchetto>\ORACLE\SCRIPT
Folder file di Deploy.sql: \\infadwhs.gbbper.priv\infa_shared\DGOV\Script\UTILITY\PackageGenerator\<Nome  Pacchetto>\ORACLE\DEPLOY

 
