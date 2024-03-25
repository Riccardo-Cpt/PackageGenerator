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
Shell aiming to create the release Package main folder and subfolders. Additionally, it writes two other shells pmrep_import_root.sh and update_return_codes.sh (they remain always the same in every release). The package name has a standard naming:

Rilascio_[release environment]_RFC_[RFC code]_[release date]

In addition, from the main folder, the generated subfolder will follows the paths:

-	./[RFC]/generico
-	./[RFC]/post script
-	./[RFC]/post script DB
-	./[RFC]/pre script
-	./[RFC code]/pre script DB
-	./ORACLE/DEPLOY
-	./ORACLE/SCRIPT
 
5.3	PackageManager.py
This script receive release tables, and from their naming calculate:
-	Involved customer areas 
-	Involved customer subareas
-	Launch WriteManifest.py
- Launch WritePmrep_import.py
 
5.3.1	WriteManifest.py
This script create the PackageManifest.xml file, a catalog of all objects that must be inculuded in the release package and need to be released

It starts writing fixed objects:
-	File header
-	Update_return_codes.sh
-	pmrep_import
-	pmrep_import_root.sh
-	In case $$WF_FLAG_FILE_MANAGER = S, objects related to file manager WF (.xml e .dtd)

Then, it will start iterating for customer areas, creating the objects:
-	Semaphore Workflows (.xml e .dtd)
-	TEST_PERMISSION Workflow (.xml e .dtd)
-	TEST_SOURCE_SYSTEM_FILE workflow (.xml e .dtd)

A nested iteration is required to work with customer subareas objects:
-	RDL WF related objects (.xml e .dtd)
-	Parameter files objects related to WF RDL (.txt)
-	Shell TEST_CONNECTION (.sh)
-	Shell TEST_CONNECTION_FILE (.sh)
-	Shell TEST_SEMAPHORE_1_2_ (.sh)
-	Shell TEST_SEMAPHORE_2_2_ (.sh)

A third nested iteration is required to get the tables for each customer subareas. With this information, it generates objects related to:
-	Shell TEST_PERMISSION (.sh)
- Shell TEST_PERMISSION_FILE (.sh)

Finally it writes:
-	File tail lines

5.3.2	WritePmrep_import.py

It writes the pmrep_import file, containing all pmprep_import commands. This script iterates each customer subarea writing the command for the related workflow. At the end of these operations, if required, it generates the pmrep_import command related to Wf file manager.

5.4	FillPackage.sh
It reads each object included in PackageManifest.xml, for each element it searches it inside customer environment and generates a copy inside the release package, under the subfolder ./generico. In details, depending on the object, it follows those procedures:

-	Shell: it searches the file inside the environment and with cp command generates a copy inside the package.
-	ParamFile: it searches the file inside the environment and with cp command generates a copy inside the package.
-	Workflow: exports the workflow with ObjectExport command from correct informatica repository indicated inside PackageManifest.xml
-	DTD files: this files are written inside the package.

Eventually, file pointings are modified, depending on the release environment
 
5.5	GenerateDeploy.sh
This shell reads Oracle script in a user defined folder, move them inside the release package and as result writes the Deploy.sql

 
