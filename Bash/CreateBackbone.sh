#!/bin/sh

###
###Script per la creazione di tutte le folder e subfolder del pacchetto di rilascio
###

function CreatePmrep_import_root(){
	echo -e '#!/bin/bash\n#V.2 - update and check return codes\n' > $1
	echo -e 'RC_FILE=rc_file.tmp\ncd /GFS/infa/infa_shared/nolio/\n' >> $1
	echo -e '#clean ReturnCode file\n>$RC_FILE\nchown infa:infa $RC_FILE\n' >> $1
	echo -e '#exec import\nsu - infa -c \042cd /GFS/infa/infa_shared/nolio/ ; ./pmrep_import\042\n' >> $1
	echo -e '#check ReturnCode file\ntypeset -i RC_NUM=$(cat $RC_FILE)\n' >> $1
	echo -e 'exit $RC_NUM' >> $1
}

function CreateReturn_codes(){
	echo -e '#!/bin/bash\n#sum the passed return code to the value in the file\n' > $1
	echo -e '#usage: update_return_codes.sh $1\n#$1: return code to sum\n' >> $1
	echo -e 'RC_FILE=rc_file.tmp\n' >> $1
	echo -e '#check if file exists\nif [ ! -f $RC_FILE ]; then\n    #create file\n    touch $RC_FILE\nfi\n' >> $1
	echo -e '#check if file is empty\nif [ ! -s $RC_FILE ]\nthen\n    #file is empty\n    echo 0 > $RC_FILE\nfi\n' >> $1
	echo -e '#read number from file\ntypeset -i RC_NUM=$(cat $RC_FILE)\n' >> $1
	echo -e '#sum the current RC_NUM and the current $1\nRC_NUM=$(($RC_NUM + $1))\necho new RC $RC_NUM\n#save in file\necho $RC_NUM > $RC_FILE' >> $1

}

########################
RFC=$1
release_date=$2
output_dir=$3
log_dir=$4
########################

Log=$log_dir"/CreateBackbone.log"

echo "###################################"
echo -e "Inizializzazione" $(basename $0)
echo -e "###################################\n"

if [ -z $RFC ]
	then echo -e 'Error: Rfc non inserita'
	exit 1
fi

#Creazione cartella principale
mkdir $output_dir

#Creazione sottocartelle ORACLE e RFC
mkdir -p $output_dir"/ORACLE/DEPLOY"
mkdir $output_dir"/ORACLE/SCRIPT"
mkdir $output_dir"/"$RFC

#sottocartelle di RFC

post_script=$output_dir"/"$RFC"/post script"
generico=$output_dir"/"$RFC"/generico"

mkdir "$generico" 
mkdir "$post_script" 
mkdir $output_dir"/"$RFC"/post script DB"
mkdir $output_dir"/"$RFC"/pre script"
mkdir $output_dir"/"$RFC"/pre script DB"

#Generazione file di pmrep_import_root.sh sotto subfolder post_script
CreatePmrep_import_root "$post_script/pmrep_import_root.sh"
if [ $? -eq 0 ]
	then 
		echo -e "pmrep_import_root creato con successo"
	else 
		echo -e "creazione pmrep_import_root fallita"
fi

#Generazione file di update_return_codes.sh sotto subfolder generico
CreateReturn_codes "$generico/update_return_codes.sh"
if [ $? -eq 0 ]
	then 
		echo -e "update_return_codes creato con successo"
	else 
		echo -e "creazione update_return_codes fallita"
fi

echo -e "\nCreazione pacchetto per RFC: "$RFC", effettuata con successo"
