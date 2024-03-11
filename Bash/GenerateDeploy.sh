#$1 Outdir, $2 LogPath
function GenerateDeploy(){
#Controllo se la directory ORACLE ha files all'interno
counter=$(find $1/ORACLE/SCRIPT | wc -l)
if [ $counter > 0 ]
then 
	echo "Files e folder in cartella: "$counter >> $2/GenerateDeploy.log
	echo -e "set define off\nset feedback on\n\nwhenever sqlerror EXIT\n" > $1/ORACLE/DEPLOY/DEPLOY.sql
	#@../SCRIPT/
	find $1/ORACLE/SCRIPT -type f | sort | sed "s|$1/ORACLE|	@..|g">> $1/ORACLE/DEPLOY/DEPLOY.sql
	#all_files=$(echo $all_files | sed 's|${1}||g')
	
	#echo $all_files >> $1/ORACLE/DEPLOY/DEPLOY.sql
	
else 
	echo "Nessun file trovato " >> $2/GenerateDeploy.log
fi
}
########################
input_dir=$1
output_dir=$2
RFC=$3
log_dir=$4
########################

echo "##########################################"
echo -e "Inizializzazione Script $(basename $0)"
echo -e "##########################################\n"

in_oracle_dir=$input_dir/Script/UTILITY/PackageGenerator/ORACLE/$RFC
out_oracle_dir=$output_dir/ORACLE

echo 'Copia files da '${in_oracle_dir}
echo -e 'Folder di destinazione dei files: '${out_oracle_dir}'/SCRIPT\n'

cp -r $in_oracle_dir/* $out_oracle_dir/SCRIPT

echo 'Generazione file di deploy'
GenerateDeploy $output_dir $log_dir

echo -e '\nEsecuzione script terminata'