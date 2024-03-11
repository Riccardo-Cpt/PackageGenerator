# PackageGenerator
Automatization of Release Package creation for a private client

This software is meant to be runned with Informatica Powercenter 

Param file: to run the software is necessary to write a list of all the tables meant to be realeased. All the tables must follow a strict naming convention.
Three variables are assigned to store lists of table names ($$V_WF_LISTA1, $$V_WF_LISTA2, $$V_WF_LISTA3), max 2000 char each

Other optional parameters are displayed in the following table:

![image](https://github.com/Riccardo-Cpt/PackageGenerator/assets/61077368/a36dbc90-6721-4bc4-88fd-be68409aea7e)

The workflow follows the following architecture:

![image](https://github.com/Riccardo-Cpt/PackageGenerator/assets/61077368/ebcb0c3a-ab05-4b09-84b0-2dd02665741c)

In thi table is shortly described each process:
![image](https://github.com/Riccardo-Cpt/PackageGenerator/assets/61077368/197f47e9-819c-43bc-a0e8-b822f27fd919)
