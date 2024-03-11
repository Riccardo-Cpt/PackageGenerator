#!/bin/sh
########################################################################
#######################FILLPACKAGE######################################
########################################################################
#Script per lo spostamento dei file elencati nel PackageManifest sotto il subfolder generico del pacchetto di rilascio


##FUNZIONE PER LA GENERAZIONE DI UN DTD GENERICO PER FOLDER IN INPUT
#$1 file scrittura, $2 folder, $3 ambiente, $4 ambiente_prec, $5 log_dir
function Generate_DTD(){

#scrittura file .DTD sotto generico
	echo -e '<?xml version="1.0" encoding="UTF-8"?> ' > $1
	echo -e '<!--DOCTYPE IMPORTPARAMS SYSTEM "impcntl.dtd"--> ' >> $1
	echo -e '<IMPORTPARAMS CHECKIN_AFTER_IMPORT="YES" CHECKIN_COMMENTS="IMPORT OBJECTS" RETAIN_GENERATED_VALUE="YES"> ' >> $1
	echo -e '<FOLDERMAP ' >> $1
	echo -e 'SOURCEFOLDERNAME="'$2'" ' >> $1
	echo -e 'SOURCEREPOSITORYNAME="REPDQ_'$4'" ' >> $1
	echo -e 'TARGETFOLDERNAME="'$2'" ' >> $1
	echo -e 'TARGETREPOSITORYNAME="REPDQ_'$3'"/> ' >> $1
	echo -e '<RESOLVECONFLICT> \n<TYPEOBJECT OBJECTTYPENAME="ALL" RESOLUTION="REPLACE"/> \n</RESOLVECONFLICT> \n</IMPORTPARAMS> ' >> $1
	
	echo -e $1 " Generato con successo\n" #>> $5/FillPackage.log
}

##FUNZIONE DISEGNATA PER IL MOVIMENTO DI BWPARAM E SHELL .sh DA AMBIENTE DI SVILUPPO/TEST A PACCHETTO DI RILASCIO
#$1 pathscript, $2 destdir,$3 log_dir
function MoveFile(){
#se il file esiste, viene spostato
if [ -f $1 ]
then 
	echo "Spostamento "$1 #>> $3/FillPackage.log
	cp $1 $2 && echo -e "Spostamento avvenuto con successo\n" #>> $3/FillPackage.log
else 
	echo "$1 non trovato " #>> $3/FillPackage.log
fi
}

########################
ambiente=$1
input_dir=$2
output_dir=$3
log_dir=$4
########################
echo "########################################"
echo -e "Inizializzazione Script $(basename $0)"
echo -e "########################################\n"

#Calcolo ambiente di origine all'interno della variabile $ambiente_prec
#Calcolo dei repository ed etldwh9 a seconda se il rilascio debba essere effettuato in test o produzione
if [ $ambiente = 'TEST' ]
		then ambiente_prec='DEV'
		repository=REPDQ_DEV
		etldwh9=ETLDWH9_SVIL
elif [ $ambiente = 'PROD' ]
		then ambiente_prec='TEST'
		repository=REPDQ_TEST
		etldwh9=ETLDWH9_TEST
else
	echo '--> ERRORE: Ambiente inserito scorretto, terminazione script'
	exit 1
fi

#Calcolo file PackageManifest in lettura
manifest=$output_dir/PackageManifest.xml
dest_dir=$output_dir/generico

#Filtraggio nomi oggetti presenti nel manifest
lines=$(grep '<filename value=' $manifest)
listaFiles=$(echo $lines | sed 's/<filename value=//g; s/"//g; s/\/>//g')

#Calcolo directory di rilascio all interno del pacchetto
#dest_dir=$output_dir/generico

#Creazione lista aree per iterazione successiva
aree=$(cat $log_dir/temp_areas.txt)
aree=$(echo $aree | sed 's/,/ /g')
echo -e 'Lista aree utilizzate: '$aree #>> $log_dir/FillPackage.log

#Loop annidiati, esterno itera per aree input, interno per tutti i file nel manifest. Per evitare iterazioni inutili, filtriamo all interno solo i file appartenenti all area corrente
#Richiamo funzione MoveFile per spostamento file .txt e .sh da directories Script o BWParam a pacchetto
for area in $aree; do

	for file in $listaFiles; do

		if [[ $file =~ _${area}[a-zA-Z0-9]_ || $file =~ _${area}[a-zA-Z0-9]. ]]; then
			if [[ $file == *.sh ]]; then 
				
				pathScript=$input_dir/Script/$area/$file
				MoveFile "$pathScript" "$dest_dir" "$log_dir"
				
			elif [[ $file == *.txt ]]; then
			
				pathParam=$input_dir/BWParam/$area/$file
				MoveFile "$pathParam" "$dest_dir" "$log_dir"
			fi
		fi

#Esportazione oggetti .xml presenti nel manifest e creazione relativi oggetti .dtd con funzione Generate_DTD
		if [[ $file =~ _${area}_ || $file =~ _$area[a-zA-Z0-9]_ ]]; then
		
			folderName='SF_IL_'$area
			if [[ $file == *.xml ]]; then
				
				workflowName=$(echo $file | sed 's/.xml//g')
				
				pmrep connect -r $repository -d $etldwh9 -n Administrator -X INFA_PW -s Native > $log_dir/Connection.log 
				pmrep ObjectExport -o workflow -f $folderName -n $workflowName -m -s -b -r -u $dest_dir/$workflowName.xml > $log_dir/Export_$workflowName.log 
				echo "Export di "$workflowName".xml effettuato" #>> $log_dir/FillPackage.log

#Invocazione funzione di generazione dei file .dtd
			elif [[ $file == *.dtd ]]; then
				
				Generate_DTD "$dest_dir/$file" "$folderName" "$ambiente" "$ambiente_prec" "$log_dir"
			fi
		fi
	done
done


#Modificazione puntamenti nei file
echo -e "\n----------------------------------------------------------" #>> $log_dir/FillPackage.log
echo -e "Modifica puntamenti file .sh .txt e .xml per ambiente"$ambiente #>> $log_dir/FillPackage.log
echo -e "----------------------------------------------------------\n" #>> $log_dir/FillPackage.log

if [[ $ambiente = 'TEST' ]]; then 
	find $dest_dir -type f -name "*.xml" -exec sed -i -e 's/ISDQ_DEV/ISDQ_TEST/g' -e 's/ETLDWH9_SVIL/ETLDWH9_TEST/g' {} +
	find $dest_dir -type f -name "*.sh" -exec sed -i -e 's/ISDQ_DEV/ISDQ_TEST/g' -e 's/ETLDWH9_SVIL/ETLDWH9_TEST/g' {} +
	find $dest_dir -type f -name "*.txt" -exec sed -i -e 's/ISDQ_DEV/ISDQ_TEST/g' -e 's/ETLDWH9_SVIL/ETLDWH9_TEST/g' {} +
elif [[ $ambiente = 'PROD' ]]; then 
	find $dest_dir -type f -name "*.xml" -exec sed -i -e 's/ISDQ_TEST/ISDQ_PROD/g' -e 's/ETLDWH9_TEST/ETLDWH9_PROD/g' {} +
	find $dest_dir -type f -name "*.sh" -exec sed -i -e 's/ISDQ_TEST/ISDQ_PROD/g' -e 's/ETLDWH9_TEST/ETLDWH9_PROD/g' {} +
	find $dest_dir -type f -name "*.txt" -exec sed -i -e 's/ISDQ_TEST/ISDQ_PROD/g' -e 's/DW_ORACLE_EDW_DWETL_STND/DW_ETL_X_ORA_EDWP_DWETL_STND/g' {} +
else 
	echo '--> ERRORE: Ambiente inserito scorretto, terminazione script'
	exit 1
fi 


#Controllo presenza WF_IL_000_FILE_MANAGER nel Manifest, se presente 2 volte (1 dtd, 1 xml) procede a crearne gli oggetti nel pacchetto
fileManger_flg=$(grep -w 'WF_IL_000_FILE_MANAGER' $manifest | wc -l)

if [[ $fileManger_flg == 2 ]]; then 
	
	#esportazione del WF. Non utilizzato attualmente in quanto richiede export da produzione
	#pmrep connect -r $repository -d $etldwh9 -n Administrator -X INFA_PW -s Native >> $log_dir/Connection.log 
	#pmrep ObjectExport -o workflow -f SF_UTILITY -n WF_IL_000_FILE_MANAGER -m -s -b -r -u $dest_dir/WF_IL_000_FILE_MANAGER.xml > $log_dir/Export_WF_IL_000_FILE_MANAGER.log
	
	#Generazione file .dtd relativo al file manager
	Generate_DTD ${dest_dir}"/DTD_WF_IL_000_FILE_MANAGER.dtd" "SF_UTILITY" "$ambiente" "$ambiente_prec" "$log_dir"

elif [[ $fileManger_flg == 0 ]]; then
	echo -e '\nATTENZIONE: File manager non censito\n'
else 
	echo -e '\nATTENZIONE: numero anomalo di occorrenze relative al workflow di file manager, count: '$fileManger_flg
	exit 1
fi
####Fine controllo file manager


echo -e "\nScript terminato con successo" #>> $log_dir/FillPackage.log